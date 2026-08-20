from __future__ import annotations

import json
from pathlib import Path
import subprocess

from scripts import grade_activity
from scripts.validate_activity import validate_activity

ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content" / "tpsi5" / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content" / "tpsi5" / "13_WEBSOCKET_SOCKETIO_REALTIME.md"
A_ROOT = ROOT / "activities" / "tpsi5" / "websocket_realtime_microscope_a"
B_ROOT = ROOT / "activities" / "tpsi5" / "realtime_event_reducer_b"
C_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_realtime_c"
D_ROOT = ROOT / "activities" / "tpsi5" / "realtime_debug_d"
FRONTEND = ROOT / "_realtime-frontend"
COMPOSED = ROOT / "_realtime-reference"
PROBE = ROOT / "tests" / "realtime_probe"
SOCKET_IO_VERSION = "4.8.3"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def assert_activity(root: Path, difficulty: str, activity_id: str, automatic: bool) -> dict:
    activity = load(root / "activity.json")
    assert validate_activity(activity, str(root / "activity.json")) == []
    assert activity["id"] == activity_id
    assert activity["difficolta"] == difficulty
    assert activity["contesto"]["uda"] == "uda-25"
    assert sum(entry["punti"] for entry in activity["rubrica"]) == 10
    assert activity["correzione"]["test"] is automatic
    for asset in activity["assets"]:
        assert (root / asset["path"]).is_file(), asset
        if asset["visibility"] == "student":
            assert asset.get("target_path")
    return activity


def test_realtime_content_pack_course_design_and_activity_contracts() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    assert pack["version"] == "0.14.0"
    decisions = pack["extensions"]["bootstrap_decisions"]
    assert decisions["frontend_framework"] == "vue3-vite"
    assert decisions["typescript_depth"] == "targeted-boundary-typing"
    assert decisions["node_orm"] == "tbd"

    refs = {entry["id"]: entry for entry in pack["references"]}
    assert refs["tpsi5-ref-websocket"]["role"] == "specification"
    assert refs["tpsi5-ref-socketio"]["role"] == "technical-reference"
    assert SOCKET_IO_VERSION in refs["tpsi5-ref-socketio"]["notes"]

    item = next(x for x in pack["content_items"] if x["id"] == "tpsi5-content-websocket-socketio-realtime")
    assert item["order"] == 14
    assert item["path"] == "content/tpsi5/13_WEBSOCKET_SOCKETIO_REALTIME.md"
    assert item["activity_ids"] == [
        "tpsi5-activity-a-websocket-realtime-microscope-001",
        "tpsi5-activity-b-realtime-event-reducer-001",
        "tpsi5-activity-c-feisbuc-socketio-realtime-001",
        "tpsi5-activity-d-debug-realtime-boundaries-001",
    ]
    assert LESSON_PATH.is_file()

    uda25 = next(u for u in design["years"][0]["udas"] if u["id"] == "uda-25")
    assert uda25["weeks"] == "5"
    assert [entry["source"] for entry in uda25["items"]] == [
        "content/tpsi5/10_VUE3_COMPONENTI_REATTIVITA.md",
        "content/tpsi5/11_VUE_ROUTER_NAVIGAZIONE_SPA.md",
        "content/tpsi5/12_TYPESCRIPT_CONTRATTI_FRONTEND.md",
        "content/tpsi5/13_WEBSOCKET_SOCKETIO_REALTIME.md",
    ]
    assert uda25["items"][3]["activity_ids"] == item["activity_ids"]

    assert_activity(A_ROOT, "A", "tpsi5-activity-a-websocket-realtime-microscope-001", False)
    b = assert_activity(B_ROOT, "B", "tpsi5-activity-b-realtime-event-reducer-001", True)
    c = assert_activity(C_ROOT, "C", "tpsi5-activity-c-feisbuc-socketio-realtime-001", False)
    assert_activity(D_ROOT, "D", "tpsi5-activity-d-debug-realtime-boundaries-001", False)
    assert b["linguaggio"] == "javascript"
    assert c["project_milestone"] == "feisbuc-12-socketio-realtime"


def test_realtime_reducer_passes_real_javascript_runner() -> None:
    activity = load(B_ROOT / "activity.json")
    report = grade_activity.grade_activity(activity, B_ROOT / "solution/main.js", timeout_seconds=5)
    assert report["passed"] is True, report
    assert report["summary"] == {
        "passed": len(activity["test_cases"]),
        "total": len(activity["test_cases"]),
    }


def test_realtime_toolchain_build_and_event_boundaries_are_explicit() -> None:
    frontend_package = load(FRONTEND / "package.json")
    backend_package = load(COMPOSED / "package.json")
    probe_package = load(PROBE / "package.json")

    assert frontend_package["dependencies"]["socket.io-client"] == SOCKET_IO_VERSION
    assert backend_package["dependencies"]["socket.io"] == SOCKET_IO_VERSION
    assert probe_package["dependencies"]["socket.io-client"] == SOCKET_IO_VERSION
    assert (FRONTEND / "node_modules" / "socket.io-client").is_dir()
    assert (FRONTEND / "dist/index.html").is_file()
    assert (COMPOSED / "node_modules" / "socket.io").is_dir()
    assert (PROBE / "node_modules" / "socket.io-client").is_dir()

    events = (C_ROOT / "solution/frontend/src/realtime-events.ts").read_text(encoding="utf-8")
    adapter = (C_ROOT / "solution/frontend/src/realtime.ts").read_text(encoding="utf-8")
    feed = (C_ROOT / "solution/frontend/src/views/FeedView.vue").read_text(encoding="utf-8")
    realtime_server = (C_ROOT / "solution/backend/src/realtime.js").read_text(encoding="utf-8")
    posts_router = (C_ROOT / "solution/backend/src/posts.router.js").read_text(encoding="utf-8")
    server = (C_ROOT / "solution/backend/src/server.js").read_text(encoding="utf-8")

    for event_name in ("post:created", "post:updated", "post:deleted"):
        assert event_name in events
        assert event_name in realtime_server
    assert "posts.some" in events
    assert "parseRealtimeEvent" in events
    assert "Invalid realtime post payload" in events
    assert "Invalid realtime delete payload" in events
    assert '(payload: unknown)' in adapter
    assert "parseRealtimeEvent(type, payload)" in adapter
    assert 'socket.on("post:create"' not in realtime_server
    assert "readCookie(socket.request.headers.cookie" in realtime_server
    assert "hashSessionToken" in realtime_server
    assert "findSessionUser(socket.data.sessionHash" in realtime_server
    assert "socket.disconnect(true)" in realtime_server
    assert 'postEvents.publish({ type: "post:created"' in posts_router
    assert 'postEvents.publish({ type: "post:updated"' in posts_router
    assert 'postEvents.publish({ type: "post:deleted"' in posts_router
    assert "createServer(app)" in server and "attachRealtime" in server

    assert "onUnmounted(() => realtime.stop())" in feed
    assert "queuedEvents" in feed
    assert "applyOrQueue" in feed
    assert "resyncPosts" in feed
    assert "resyncRequested" in feed
    assert "onConnect()" in feed and "onReconnect()" in feed
    assert feed.count("void resyncPosts()") >= 3
    assert "applyRealtimeEvent" in feed
    assert "snapshot successivo all'handshake effettivo" in feed
    assert "localStorage" not in adapter and "document.cookie" not in adapter


def test_realtime_debug_fixture_encodes_security_lifecycle_and_recovery_failures() -> None:
    broken_server = (D_ROOT / "starter/server.js").read_text(encoding="utf-8")
    broken_client = (D_ROOT / "starter/client.ts").read_text(encoding="utf-8")
    fixed_server = (D_ROOT / "solution/server.js").read_text(encoding="utf-8")
    fixed_client = (D_ROOT / "solution/client.ts").read_text(encoding="utf-8")
    diagnosis = (D_ROOT / "solution/DIAGNOSI.md").read_text(encoding="utf-8").lower()

    assert 'cors: { origin: "*" }' in broken_server
    assert 'socket.on("post:create"' in broken_server
    assert "payload.authorId" in broken_server
    assert 'socket.on("post:created"' in broken_client
    assert "posts.unshift(post)" in broken_client
    assert 'socket.emit("post:create"' in broken_client

    assert 'socket.on("post:create"' not in fixed_server
    assert "verifySocketSession" in fixed_server
    assert 'fetch("/api/posts"' in fixed_client
    assert 'socket.off("post:created"' in fixed_client
    for concept in ("security", "lifecycle", "delivery", "recovery", "architecture", "idempotente"):
        assert concept in diagnosis


def test_two_authenticated_socket_clients_receive_rest_domain_events_and_resync() -> None:
    result = subprocess.run(
        ["node", "probe.mjs", str(COMPOSED)],
        cwd=PROBE,
        capture_output=True,
        text=True,
        timeout=45,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert payload["ok"] is True
    assert payload["anonymousRejected"] is True
    assert payload["updated"] is True
    assert payload["deleted"] is True
    assert payload["forgedSocketCommandRejected"] is True
    assert payload["resyncRecovered"]
