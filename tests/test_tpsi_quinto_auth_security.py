from __future__ import annotations

from contextlib import closing
import hashlib
import http.cookiejar
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import tempfile
import urllib.error
import urllib.request

import pytest

from scripts import grade_activity
from scripts.validate_activity import validate_activity

ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content/tpsi5/content-pack.json"
DESIGN_PATH = ROOT / "doc/course_designs/tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content/tpsi5/08_AUTH_SESSIONI_SICUREZZA.md"
A_ROOT = ROOT / "activities/tpsi5/auth_credential_policy_a"
B_ROOT = ROOT / "activities/tpsi5/auth_post_authorization_b"
C_ROOT = ROOT / "activities/tpsi5/feisbuc_auth_c"
D_ROOT = ROOT / "activities/tpsi5/auth_debug_d"
PASSWORD = "una passphrase lunga 2026"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class RunningAuthServer:
    def __init__(self, *, db_path: Path, extra_env: dict[str, str] | None = None):
        env = dict(os.environ)
        env.update({
            "PORT": "0",
            "DB_PATH": str(db_path),
            "NODE_ENV": "development",
            "COOKIE_SECURE": "false",
            "SESSION_TTL_MS": str(8 * 60 * 60 * 1000),
        })
        if extra_env:
            env.update(extra_env)
        server = C_ROOT / "solution/src/server.js"
        self.process = subprocess.Popen(
            ["node", server.name],
            cwd=server.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        assert self.process.stdout is not None
        line = self.process.stdout.readline().strip()
        if not line.startswith("READY http://"):
            stderr = self.process.stderr.read() if self.process.stderr else ""
            self.close()
            raise AssertionError(f"auth server non pronto: {line!r} stderr={stderr!r}")
        self.base = line.removeprefix("READY ")

    def close(self) -> None:
        if self.process.poll() is not None:
            return
        self.process.terminate()
        try:
            self.process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=5)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


def new_client():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    return opener, jar


def call(opener, url: str, *, method: str = "GET", payload=None, headers: dict[str, str] | None = None):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request_headers = dict(headers or {})
    if payload is not None:
        request_headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=request_headers, method=method)
    response = opener.open(req, timeout=15)
    raw = response.read()
    media = response.headers.get_content_type()
    value = json.loads(raw.decode("utf-8")) if raw and media == "application/json" else raw.decode("utf-8")
    return response.status, response.headers, value


def error_call(opener, url: str, **kwargs):
    with pytest.raises(urllib.error.HTTPError) as exc:
        call(opener, url, **kwargs)
    error = exc.value
    raw = error.read()
    media = error.headers.get_content_type()
    value = json.loads(raw.decode("utf-8")) if raw and media == "application/json" else raw.decode("utf-8")
    return error.code, error.headers, value


def assert_activity(root: Path, difficulty: str, activity_id: str, automatic: bool) -> dict:
    activity = load(root / "activity.json")
    assert validate_activity(activity, str(root / "activity.json")) == []
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
    assert activity["correzione"]["test"] is automatic
    return activity


def cookie_value(jar: http.cookiejar.CookieJar, name: str = "feisbuc.sid") -> str:
    matches = [cookie.value for cookie in jar if cookie.name == name]
    assert len(matches) == 1, [(cookie.name, cookie.value) for cookie in jar]
    return matches[0]


def test_auth_content_pack_design_and_activity_contracts() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    item = next(x for x in pack["content_items"] if x["id"] == "tpsi5-content-auth-sessions-security")
    assert pack["version"] == "0.11.0"
    assert item["path"] == "content/tpsi5/08_AUTH_SESSIONI_SICUREZZA.md"
    assert item["order"] == 9
    assert item["activity_ids"] == [
        "tpsi5-activity-a-auth-credential-policy-001",
        "tpsi5-activity-b-auth-post-authorization-001",
        "tpsi5-activity-c-feisbuc-auth-session-001",
        "tpsi5-activity-d-debug-auth-security-001",
    ]
    refs = {ref["id"] for ref in item["source_refs"]}
    assert {
        "tpsi5-ref-nist-800-63b",
        "tpsi5-ref-owasp-password-storage",
        "tpsi5-ref-owasp-session-management",
        "tpsi5-ref-owasp-csrf",
        "tpsi5-ref-mdn-cookies",
        "tpsi5-ref-node",
        "tpsi5-ref-express",
        "tpsi5-ref-sqlite",
        "tpsi5-ref-lab9-legacy",
    } <= refs
    assert LESSON_PATH.is_file()

    uda24 = next(u for u in design["years"][0]["udas"] if u["id"] == "uda-24")
    assert uda24["weeks"] == "7"
    assert len(uda24["items"]) == 4
    auth_item = uda24["items"][2]
    assert auth_item["source"] == "content/tpsi5/08_AUTH_SESSIONI_SICUREZZA.md"
    assert auth_item["activity_ids"] == item["activity_ids"]
    assert "SSR" in auth_item["frame"]["next_step"]
    assert uda24["items"][3]["source"] == "content/tpsi5/09_SSR_NUNJUCKS_CONFRONTO.md"

    a = assert_activity(A_ROOT, "A", "tpsi5-activity-a-auth-credential-policy-001", True)
    b = assert_activity(B_ROOT, "B", "tpsi5-activity-b-auth-post-authorization-001", True)
    c = assert_activity(C_ROOT, "C", "tpsi5-activity-c-feisbuc-auth-session-001", False)
    d = assert_activity(D_ROOT, "D", "tpsi5-activity-d-debug-auth-security-001", False)
    assert a["linguaggio"] == b["linguaggio"] == "javascript"
    assert c["project_milestone"] == "feisbuc-07-auth-session"
    assert d["tipo"] == "debug-didattico"


def test_auth_pure_reference_solutions_pass_real_javascript_runner() -> None:
    for root in (A_ROOT, B_ROOT):
        activity = load(root / "activity.json")
        report = grade_activity.grade_activity(activity, root / "solution/main.js", timeout_seconds=5)
        assert report["passed"] is True, report
        assert report["summary"] == {
            "passed": len(activity["test_cases"]),
            "total": len(activity["test_cases"]),
        }


def test_password_service_uses_random_salt_scrypt_and_verifies() -> None:
    source = C_ROOT / "solution/src/passwords.js"
    runner = """
import { hashPassword, verifyPassword, PASSWORD_KDF } from './passwords.js';
const a = await hashPassword(process.argv[2]);
const b = await hashPassword(process.argv[2]);
const ok = await verifyPassword(process.argv[2], a);
const wrong = await verifyPassword('password completamente diversa', a);
console.log(JSON.stringify({a,b,ok,wrong,kdf:PASSWORD_KDF}));
"""
    runner_path = source.parent / "__auth_test_runner.mjs"
    try:
        runner_path.write_text(runner, encoding="utf-8")
        result = subprocess.run(
            ["node", runner_path.name, PASSWORD],
            cwd=source.parent,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    finally:
        runner_path.unlink(missing_ok=True)
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["a"].startswith("scrypt$16384$8$5$")
    assert payload["b"].startswith("scrypt$16384$8$5$")
    assert payload["a"] != payload["b"]
    assert payload["ok"] is True and payload["wrong"] is False
    assert payload["kdf"] == {
        "algorithm": "scrypt",
        "cost": 16384,
        "blockSize": 8,
        "parallelization": 5,
        "keyLength": 32,
    }


def test_production_config_fails_closed_without_secure_cookie() -> None:
    config = C_ROOT / "solution/src/config.js"
    script = "import {loadConfig} from './config.js'; try { console.log(JSON.stringify(loadConfig(process.env))); } catch(e) { console.error(e.message); process.exit(17); }"
    insecure = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=config.parent,
        env={**os.environ, "NODE_ENV": "production", "COOKIE_SECURE": "false"},
        capture_output=True, text=True, timeout=10, check=False,
    )
    assert insecure.returncode == 17
    assert "COOKIE_SECURE" in insecure.stderr

    secure = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=config.parent,
        env={**os.environ, "NODE_ENV": "production", "COOKIE_SECURE": "true"},
        capture_output=True, text=True, timeout=10, check=False,
    )
    assert secure.returncode == 0, secure.stderr
    parsed = json.loads(secure.stdout)
    assert parsed["cookieSecure"] is True
    assert parsed["cookieName"] == "__Host-feisbuc.sid"


def test_auth_reference_e2e_cookie_db_ownership_logout_and_restart() -> None:
    assert (C_ROOT / "solution/node_modules/express").is_dir(), "npm install CI auth mancante"

    with tempfile.TemporaryDirectory() as temp:
        db_path = Path(temp) / "auth-e2e.db"
        alice, alice_jar = new_client()
        bob, bob_jar = new_client()

        with RunningAuthServer(db_path=db_path) as server:
            code, _, payload = error_call(alice, f"{server.base}/api/auth/me")
            assert code == 401 and payload["error"]["code"] == "authentication-required"
            code, _, payload = error_call(alice, f"{server.base}/api/posts")
            assert code == 401

            code, _, payload = error_call(
                alice,
                f"{server.base}/api/auth/register",
                method="POST",
                payload={"displayName":"Alice","email":"alice@example.test","password":"TroppoCorta1!"},
            )
            assert code == 400 and payload["error"]["code"] == "registration-invalid"

            status, headers, alice_payload = call(
                alice,
                f"{server.base}/api/auth/register",
                method="POST",
                payload={"displayName":"Alice","email":"ALICE@Example.Test","password":PASSWORD},
            )
            assert status == 201
            assert alice_payload["user"]["email"] == "alice@example.test"
            assert set(alice_payload["user"]) == {"id","email","displayName"}
            set_cookie = headers.get("Set-Cookie")
            assert set_cookie
            lower_cookie = set_cookie.lower()
            assert "httponly" in lower_cookie and "samesite=strict" in lower_cookie and "path=/" in lower_cookie
            assert "secure" not in lower_cookie
            assert headers.get("Cache-Control") == "no-store"
            alice_id = alice_payload["user"]["id"]
            alice_token = cookie_value(alice_jar)

            status, _, me = call(alice, f"{server.base}/api/auth/me")
            assert status == 200 and me["user"]["id"] == alice_id

            status, _, created = call(
                alice,
                f"{server.base}/api/posts",
                method="POST",
                payload={"text":"post di Alice", "authorId":"spoofed-client-id"},
            )
            assert status == 201
            assert created["authorId"] == alice_id
            assert created["author"] == "Alice"
            post_id = created["id"]

            status, _, bob_payload = call(
                bob,
                f"{server.base}/api/auth/register",
                method="POST",
                payload={"displayName":"Bob","email":"bob@example.test","password":"altra passphrase lunga 2026"},
            )
            assert status == 201
            bob_id = bob_payload["user"]["id"]
            assert bob_id != alice_id

            code, _, forbidden = error_call(bob, f"{server.base}/api/posts/{post_id}", method="DELETE")
            assert code == 403 and forbidden["error"]["code"] == "forbidden"

            code, _, cross_site = error_call(
                alice,
                f"{server.base}/api/posts",
                method="POST",
                payload={"text":"cross site"},
                headers={"Sec-Fetch-Site":"cross-site"},
            )
            assert code == 403 and cross_site["error"]["code"] == "cross-site-request-blocked"

            status, _, _ = call(alice, f"{server.base}/api/posts/{post_id}", method="DELETE")
            assert status == 204

            _, _, persistent_post = call(alice, f"{server.base}/api/posts", method="POST", payload={"text":"resta dopo restart"})
            persistent_id = persistent_post["id"]

        assert db_path.is_file()
        with closing(sqlite3.connect(db_path)) as db:
            email, password_hash = db.execute(
                "SELECT email, password_hash FROM users WHERE id = ?", (alice_id,)
            ).fetchone()
            assert email == "alice@example.test"
            assert password_hash != PASSWORD
            assert password_hash.startswith("scrypt$16384$8$5$")
            session_hashes = [row[0] for row in db.execute("SELECT id_hash FROM sessions")]
            assert session_hashes
            assert all(re.fullmatch(r"[0-9a-f]{64}", value) for value in session_hashes)
            assert alice_token not in session_hashes
            assert hashlib.sha256(alice_token.encode()).hexdigest() in session_hashes

        with RunningAuthServer(db_path=db_path) as restarted:
            status, _, me = call(alice, f"{restarted.base}/api/auth/me")
            assert status == 200 and me["user"]["id"] == alice_id
            status, _, posts = call(alice, f"{restarted.base}/api/posts")
            assert status == 200 and persistent_id in {post["id"] for post in posts}

            old_token = cookie_value(alice_jar)
            status, logout_headers, _ = call(alice, f"{restarted.base}/api/auth/logout", method="POST")
            assert status == 204 and logout_headers.get("Cache-Control") == "no-store"
            code, _, payload = error_call(alice, f"{restarted.base}/api/auth/me")
            assert code == 401 and payload["error"]["code"] == "authentication-required"

            code1, _, wrong_user = error_call(
                alice, f"{restarted.base}/api/auth/login", method="POST",
                payload={"email":"missing@example.test","password":PASSWORD},
            )
            code2, _, wrong_password = error_call(
                alice, f"{restarted.base}/api/auth/login", method="POST",
                payload={"email":"alice@example.test","password":"questa password e sbagliata ma lunga"},
            )
            assert code1 == code2 == 401
            assert wrong_user["error"]["code"] == wrong_password["error"]["code"] == "invalid-credentials"

            status, _, _ = call(
                alice, f"{restarted.base}/api/auth/login", method="POST",
                payload={"email":"alice@example.test","password":PASSWORD},
            )
            assert status == 200
            new_token = cookie_value(alice_jar)
            assert new_token != old_token


def test_auth_reference_does_not_move_session_secret_into_client_or_add_identity_frameworks() -> None:
    package = load(C_ROOT / "solution/package.json")
    assert package["dependencies"] == {"express": "5.2.1"}
    client = "\n".join(path.read_text(encoding="utf-8") for path in (C_ROOT / "solution/public").glob("*.js"))
    server = "\n".join(path.read_text(encoding="utf-8") for path in (C_ROOT / "solution/src").glob("*.js"))
    assert "localStorage" not in client and "sessionStorage" not in client
    assert "document.cookie" not in client
    assert "credentials: \"same-origin\"" in client
    assert "req.body.authorId" not in server
    assert "req.auth.user.id" in server
    assert "timingSafeEqual" in server and "randomBytes(32)" in server
    for forbidden in ("jsonwebtoken", "passport", "express-session", "cookie-parser", "sequelize", "prisma", "drizzle"):
        assert forbidden not in server.lower()


def test_security_review_covers_required_trust_failures() -> None:
    insecure = (D_ROOT / "starter/insecure.js").read_text(encoding="utf-8")
    review = (D_ROOT / "solution/SECURITY_REVIEW.md").read_text(encoding="utf-8").lower()
    assert "password TEXT" in insecure
    assert "sessionId = user.id" in insecure
    assert "req.body.authorId" in insecure
    for concept in (
        "plaintext", "enumeration", "randombytes", "httponly", "secret", "impersonation", "idor", "revoc"
    ):
        assert concept in review
