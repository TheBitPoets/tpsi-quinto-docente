from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
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
LESSON_PATH = ROOT / "content/tpsi5/07_SQL_RAW_PERSISTENCE.md"
A_ROOT = ROOT / "activities/tpsi5/sql_posts_schema_a"
B_ROOT = ROOT / "activities/tpsi5/sql_posts_dml_b"
C_ROOT = ROOT / "activities/tpsi5/feisbuc_sql_c"
D_ROOT = ROOT / "activities/tpsi5/sql_debug_d"


def load(path: Path) -> dict:
    value=json.loads(path.read_text(encoding="utf-8")); assert isinstance(value,dict); return value


class RunningServer:
    def __init__(self, server: Path, *, extra_env=None):
        env=dict(os.environ); env["PORT"]="0"; env.update(extra_env or {})
        self.process=subprocess.Popen(["node",server.name],cwd=server.parent,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env)
        assert self.process.stdout is not None
        line=self.process.stdout.readline().strip()
        if not line.startswith("READY http://"):
            stderr=self.process.stderr.read() if self.process.stderr else ""; self.close(); raise AssertionError(f"server non pronto {line!r}: {stderr}")
        self.base=line.removeprefix("READY ")
    def close(self):
        if self.process.poll() is not None:return
        self.process.terminate()
        try:self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:self.process.kill();self.process.wait(timeout=5)
    def __enter__(self):return self
    def __exit__(self,*_):self.close()


def request(url, *, method="GET", payload=None, content_type=None):
    data=None if payload is None else json.dumps(payload).encode()
    headers={"Content-Type":content_type} if content_type else {}
    req=urllib.request.Request(url,data=data,headers=headers,method=method)
    res=urllib.request.urlopen(req,timeout=5); body=res.read(); mt=res.headers.get_content_type()
    value=json.loads(body.decode()) if body and mt=="application/json" else body.decode()
    return res.status,res.headers,value


def assert_activity(root,difficulty,activity_id,automatic):
    activity=load(root/"activity.json")
    assert validate_activity(activity,str(root/"activity.json"))==[]
    assert activity["id"]==activity_id and activity["difficolta"]==difficulty
    assert sum(x["punti"] for x in activity["rubrica"])==10
    for asset in activity["assets"]: assert (root/asset["path"]).is_file(),asset
    assert activity["correzione"]["test"] is automatic
    return activity


def test_sql_content_pack_item_course_design_and_activity_contracts():
    pack=load(PACK_PATH); design=load(DESIGN_PATH)
    item=next(x for x in pack["content_items"] if x["id"]=="tpsi5-content-sql-raw-persistence")
    assert pack["version"]=="0.17.0"
    assert item["path"]=="content/tpsi5/07_SQL_RAW_PERSISTENCE.md" and item["order"]==8
    assert item["activity_ids"]==[
        "tpsi5-activity-a-sql-posts-schema-001","tpsi5-activity-b-sql-posts-dml-001",
        "tpsi5-activity-c-feisbuc-sql-repository-001","tpsi5-activity-d-debug-sql-state-001"]
    assert {"tpsi5-ref-lab8-legacy","tpsi5-ref-node","tpsi5-ref-sqlite"} <= {r["id"] for r in item["source_refs"]}
    assert LESSON_PATH.is_file()
    uda24=next(u for u in design["years"][0]["udas"] if u["id"]=="uda-24")
    assert len(uda24["items"])==4
    assert uda24["items"][1]["source"]=="content/tpsi5/07_SQL_RAW_PERSISTENCE.md"
    assert uda24["items"][2]["source"]=="content/tpsi5/08_AUTH_SESSIONI_SICUREZZA.md"
    assert uda24["items"][3]["source"]=="content/tpsi5/09_SSR_NUNJUCKS_CONFRONTO.md"
    assert_activity(A_ROOT,"A","tpsi5-activity-a-sql-posts-schema-001",True)
    assert_activity(B_ROOT,"B","tpsi5-activity-b-sql-posts-dml-001",True)
    c=assert_activity(C_ROOT,"C","tpsi5-activity-c-feisbuc-sql-repository-001",False)
    assert_activity(D_ROOT,"D","tpsi5-activity-d-debug-sql-state-001",True)
    assert c["project_milestone"]=="feisbuc-06-sql-persistence"


def test_sql_reference_solutions_pass_real_thebitlab_sql_runner():
    assert grade_activity.SUPPORTED_LANGUAGES["sql"]=="implemented"
    for root in (A_ROOT,B_ROOT,D_ROOT):
        activity=load(root/"activity.json")
        report=grade_activity.grade_activity(activity,root/"solution/main.sql",timeout_seconds=5)
        assert report["passed"] is True,report
        assert report["summary"]=={"passed":len(activity["test_cases"]),"total":len(activity["test_cases"])}


def test_schema_debug_and_node_sqlite_invariants():
    schema=(A_ROOT/"solution/main.sql").read_text().lower(); diagnosis=(D_ROOT/"solution/DIAGNOSI.md").read_text().lower()
    for fragment in (") strict;","check (length(trim(text)) between 1 and 280)","check (likes >= 0)","check (liked in (0, 1))","idx_posts_liked_created"):
        assert fragment in schema
    for concept in ("constraint","update","where","delete"): assert concept in diagnosis
    result=subprocess.run(["node","--input-type=module","-e","import {DatabaseSync} from 'node:sqlite'; const db=new DatabaseSync(':memory:'); db.exec('SELECT 1'); db.close(); console.log('ok')"],capture_output=True,text=True,timeout=10)
    assert result.returncode==0,result.stderr


def test_sql_repository_boundary_and_no_orm():
    package=load(C_ROOT/"solution/package.json")
    assert package["dependencies"]=={"express":"5.2.1"} and package["engines"]["node"]==">=22.13"
    store=(C_ROOT/"solution/src/sql-post-store.js").read_text(); router=(C_ROOT/"solution/src/posts.router.js").read_text(); config=(C_ROOT/"solution/src/config.js").read_text()
    assert 'from "node:sqlite"' in store and ".prepare(" in store and "WHERE id = ?" in store
    assert "req." not in store and "res." not in store and "node:sqlite" not in router
    assert "DB_PATH" in config and "C:\\" not in config
    text="\n".join(p.read_text().lower() for p in (C_ROOT/"solution/src").glob("*.js"))
    for forbidden in ("sequelize","prisma","drizzle","typeorm"):assert forbidden not in text


def test_feisbuc_sql_reference_persists_across_process_restart():
    assert (C_ROOT/"solution/node_modules/express").is_dir(),"npm install CI mancante"
    with tempfile.TemporaryDirectory() as temp:
        db_path=Path(temp)/"feisbuc.db"; env={"DB_PATH":str(db_path)}
        with RunningServer(C_ROOT/"solution/src/server.js",extra_env=env) as server:
            _,_,before=request(f"{server.base}/api/posts"); assert len(before)==1
            status,_,created=request(f"{server.base}/api/posts",method="POST",payload={"text":"persist"},content_type="application/json"); assert status==201
            created_id=created["id"]
            _,_,updated=request(f"{server.base}/api/posts/{created_id}",method="PATCH",payload={"liked":True},content_type="application/json")
            assert updated["liked"] is True and updated["likes"]==1
        assert db_path.is_file()
        with RunningServer(C_ROOT/"solution/src/server.js",extra_env=env) as server:
            _,_,posts=request(f"{server.base}/api/posts"); by_id={x["id"]:x for x in posts}
            assert created_id in by_id and by_id[created_id]["liked"] is True
            assert sum(x["id"]=="seed-1" for x in posts)==1


def test_memory_database_mode_is_isolated_between_processes():
    env={"DB_PATH":":memory:"}
    with RunningServer(C_ROOT/"solution/src/server.js",extra_env=env) as server:
        _,_,created=request(f"{server.base}/api/posts",method="POST",payload={"text":"volatile"},content_type="application/json"); volatile=created["id"]
    with RunningServer(C_ROOT/"solution/src/server.js",extra_env=env) as server:
        _,_,posts=request(f"{server.base}/api/posts"); assert volatile not in {x["id"] for x in posts}
