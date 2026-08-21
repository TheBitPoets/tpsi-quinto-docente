from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import urllib.error
import urllib.request

import pytest

from scripts import grade_activity
from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content" / "tpsi5" / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content" / "tpsi5" / "06_NODE_EXPRESS_BACKEND.md"
A_ROOT = ROOT / "activities" / "tpsi5" / "node_http_express_a"
B_ROOT = ROOT / "activities" / "tpsi5" / "post_validation_b"
C_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_express_c"
D_ROOT = ROOT / "activities" / "tpsi5" / "express_debug_d"
EXPRESS_VERSION = "5.2.1"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class RunningServer:
    def __init__(self, server: Path):
        env = dict(os.environ)
        env["PORT"] = "0"
        self.process = subprocess.Popen(
            ["node", server.name], cwd=server.parent,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env,
        )
        assert self.process.stdout is not None
        line = self.process.stdout.readline().strip()
        if not line.startswith("READY http://"):
            stderr = self.process.stderr.read() if self.process.stderr else ""
            self.close()
            raise AssertionError(f"server non pronto: {line!r} stderr={stderr!r}")
        self.base = line.removeprefix("READY ")

    def close(self) -> None:
        if self.process.poll() is not None: return
        self.process.terminate()
        try: self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill(); self.process.wait(timeout=5)

    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): self.close()


def request(url: str, *, method: str = "GET", payload=None, raw=None, content_type=None):
    data = raw
    if raw is None and payload is not None: data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": content_type} if content_type else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    response = urllib.request.urlopen(req, timeout=5)
    body = response.read(); media_type = response.headers.get_content_type()
    decoded = json.loads(body.decode("utf-8")) if body and media_type == "application/json" else body.decode("utf-8")
    return response.status, response.headers, decoded


def error_response(error: urllib.error.HTTPError):
    body = error.read(); media_type = error.headers.get_content_type()
    decoded = json.loads(body.decode("utf-8")) if body and media_type == "application/json" else body.decode("utf-8")
    return error.code, error.headers, decoded


def assert_activity(root: Path, difficulty: str, activity_id: str, automatic: bool) -> dict:
    path = root / "activity.json"; activity = load(path)
    assert validate_activity(activity, str(path)) == []
    assert activity["id"] == activity_id
    assert activity["difficolta"] == difficulty
    assert sum(entry["punti"] for entry in activity["rubrica"]) == 10
    targets = set()
    for asset in activity["assets"]:
        assert (root / asset["path"]).is_file(), asset
        if asset["visibility"] == "student":
            target = asset.get("target_path")
            assert isinstance(target, str) and target and target not in targets
            targets.add(target)
        else:
            assert asset["visibility"] == "teacher"
    if automatic:
        assert activity["correzione"]["test"] is True
        assert activity["correzione"]["sandbox"] is True
        assert activity["test_cases"]
    else:
        assert activity["correzione"] == {"compila":False,"test":False,"sandbox":False,"ai_feedback":False}
    return activity


def test_node_express_content_item_remains_first_uda24_backend_step() -> None:
    pack = load(PACK_PATH); design = load(DESIGN_PATH)
    item = next(item for item in pack["content_items"] if item["id"] == "tpsi5-content-node-express-backend")
    assert pack["version"] == "0.16.0"
    assert item["path"] == "content/tpsi5/06_NODE_EXPRESS_BACKEND.md"
    assert item["order"] == 7
    assert item["activity_ids"] == [
        "tpsi5-activity-a-node-http-express-map-001","tpsi5-activity-b-post-validation-001",
        "tpsi5-activity-c-feisbuc-express-api-001","tpsi5-activity-d-debug-express-pipeline-001",
    ]
    assert LESSON_PATH.is_file()
    uda24 = next(uda for uda in design["years"][0]["udas"] if uda["id"] == "uda-24")
    assert [entry["source"] for entry in uda24["items"]] == [
        "content/tpsi5/06_NODE_EXPRESS_BACKEND.md",
        "content/tpsi5/07_SQL_RAW_PERSISTENCE.md",
        "content/tpsi5/08_AUTH_SESSIONI_SICUREZZA.md",
        "content/tpsi5/09_SSR_NUNJUCKS_CONFRONTO.md",
    ]
    assert uda24["items"][0]["activity_ids"] == item["activity_ids"]
    assert_activity(A_ROOT,"A","tpsi5-activity-a-node-http-express-map-001",False)
    b=assert_activity(B_ROOT,"B","tpsi5-activity-b-post-validation-001",True)
    c=assert_activity(C_ROOT,"C","tpsi5-activity-c-feisbuc-express-api-001",False)
    assert_activity(D_ROOT,"D","tpsi5-activity-d-debug-express-pipeline-001",False)
    assert b["linguaggio"] == "javascript"
    assert c["project_milestone"] == "feisbuc-05-express-api"


def test_express_version_is_pinned_and_milestone5_stays_memory_only() -> None:
    for path in (A_ROOT/"starter/package.json",C_ROOT/"starter/package.json",C_ROOT/"solution/package.json",D_ROOT/"starter/package.json",D_ROOT/"solution/package.json"):
        package=load(path); assert package["dependencies"]["express"]==EXPRESS_VERSION; assert package["type"]=="module"
    source="\n".join(path.read_text(encoding="utf-8") for path in (C_ROOT/"solution/src").glob("*.js")).lower()
    for forbidden in ("node:sqlite","sequelize","prisma","drizzle","nunjucks","bcrypt","jsonwebtoken"):
        assert forbidden not in source


def test_validation_solution_passes_real_javascript_runner() -> None:
    assert shutil.which("node") is not None
    activity=load(B_ROOT/"activity.json")
    report=grade_activity.grade_activity(activity,B_ROOT/"solution/main.js",timeout_seconds=5)
    assert report["passed"] is True, report
    assert report["summary"]=={"passed":len(activity["test_cases"]),"total":len(activity["test_cases"])}


def test_native_and_express_servers_preserve_same_observable_contract() -> None:
    for server_path in (A_ROOT/"starter/native-server.js",A_ROOT/"starter/express-server.js"):
        with RunningServer(server_path) as server:
            status,headers,health=request(f"{server.base}/api/health")
            assert status==200 and headers.get_content_type()=="application/json" and health["ok"] is True
            status,_,echo=request(f"{server.base}/api/echo",method="POST",payload={"message":"same-contract"},content_type="application/json")
            assert status==200 and echo["received"]=={"message":"same-contract"}
            with pytest.raises(urllib.error.HTTPError) as missing: urllib.request.urlopen(f"{server.base}/missing",timeout=5)
            code,headers,payload=error_response(missing.value)
            assert code==404 and headers.get_content_type()=="application/json" and payload["error"]=="not-found"


def test_feisbuc_express_reference_preserves_rest_contract_and_error_model() -> None:
    assert (C_ROOT/"solution/node_modules/express").is_dir(), "npm install CI mancante"
    with RunningServer(C_ROOT/"solution/src/server.js") as server:
        status,headers,html=request(f"{server.base}/")
        assert status==200 and "Feisbuc" in html and headers["X-Request-Id"]
        status,_,posts=request(f"{server.base}/api/posts"); assert status==200 and len(posts)==1
        status,headers,created=request(f"{server.base}/api/posts",method="POST",payload={"text":"  Express CI  "},content_type="application/json")
        assert status==201 and headers["Location"]==f"/api/posts/{created['id']}" and created["text"]=="Express CI"
        status,_,updated=request(f"{server.base}/api/posts/{created['id']}",method="PATCH",payload={"liked":True},content_type="application/json")
        assert status==200 and updated["liked"] is True and updated["likes"]==1
        with pytest.raises(urllib.error.HTTPError) as missing:
            request(f"{server.base}/api/posts/missing",method="PATCH",payload={"liked":True},content_type="application/json")
        code,_,payload=error_response(missing.value); assert code==404 and payload["error"]["code"]=="post-not-found"


def test_feisbuc_express_reference_keeps_store_replaceable_and_middleware_ordered() -> None:
    app=(C_ROOT/"solution/src/app.js").read_text(encoding="utf-8")
    router=(C_ROOT/"solution/src/posts.router.js").read_text(encoding="utf-8")
    validation=(C_ROOT/"solution/src/validation.js").read_text(encoding="utf-8")
    store=(C_ROOT/"solution/src/post-store.js").read_text(encoding="utf-8")
    middleware=(C_ROOT/"solution/src/middleware.js").read_text(encoding="utf-8")
    fragments=["app.use(requestContext)","app.use(requestLogger)","app.use(express.json", "app.use(express.static",'app.use("/api/posts"',"app.use(notFound)","app.use(errorHandler)"]
    positions=[app.index(fragment) for fragment in fragments]; assert positions==sorted(positions)
    assert "postStore" in router and "new MemoryPostStore" not in router and "randomUUID" not in router
    assert "express" not in validation.lower() and "express" not in store.lower()
    assert "function errorHandler(error, req, res, next)" in middleware and "X-Request-Id" in middleware


def test_express_debug_solution_fixes_pipeline_and_preserves_safe_get() -> None:
    assert (D_ROOT/"solution/node_modules/express").is_dir(), "npm install CI mancante"
    broken=(D_ROOT/"starter/server.js").read_text(encoding="utf-8")
    fixed=(D_ROOT/"solution/server.js").read_text(encoding="utf-8")
    diagnosis=(D_ROOT/"solution/DIAGNOSI.md").read_text(encoding="utf-8")
    assert broken.index('app.use("/api/posts", router)') < broken.index("app.use(express.json())")
    assert "req.query.id" in broken and 'router.get("/create"' in broken and "app.use((error, req, res)" in broken
    assert fixed.index("app.use(express.json())") < fixed.index('app.use("/api/posts", router)')
    assert "req.params.id" in fixed and 'router.get("/create"' not in fixed and "app.use((error, req, res, next)" in fixed
    for concept in ("express.json","req.params","GET","express.static","quattro argomenti"): assert concept.lower() in diagnosis.lower()
    with RunningServer(D_ROOT/"solution/server.js") as server:
        status,_,html=request(f"{server.base}/"); assert status==200 and "Debug Express" in html
        status,_,posts=request(f"{server.base}/api/posts"); before=len(posts)
        with pytest.raises(urllib.error.HTTPError) as create_get: urllib.request.urlopen(f"{server.base}/api/posts/create?text=x",timeout=5)
        assert create_get.value.code==404
        status,_,after=request(f"{server.base}/api/posts"); assert status==200 and len(after)==before
