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
LESSON_PATH = ROOT / "content/tpsi5/05_HTTP_ASYNC_FETCH_REST.md"
A_ROOT = ROOT / "activities/tpsi5/http_microscope_a"
B_ROOT = ROOT / "activities/tpsi5/async_response_b"
C_ROOT = ROOT / "activities/tpsi5/feisbuc_rest_c"
D_ROOT = ROOT / "activities/tpsi5/fetch_debug_d"


def load(path: Path) -> dict:
    value=json.loads(path.read_text(encoding="utf-8")); assert isinstance(value,dict); return value


class RunningServer:
    def __init__(self, server: Path):
        env=dict(os.environ); env["PORT"]="0"
        self.process=subprocess.Popen(["node",server.name],cwd=server.parent,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env)
        assert self.process.stdout is not None
        line=self.process.stdout.readline().strip()
        if not line.startswith("READY http://"):
            stderr=self.process.stderr.read() if self.process.stderr else ""; self.close(); raise AssertionError(f"server non pronto: {line!r} {stderr}")
        self.base=line.removeprefix("READY ")
    def close(self):
        if self.process.poll() is not None:return
        self.process.terminate()
        try:self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:self.process.kill();self.process.wait(timeout=5)
    def __enter__(self):return self
    def __exit__(self,*_):self.close()


def request(url,*,method="GET",payload=None,content_type=None):
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


def test_uda23_content_item_remains_stable_after_later_backend_increments():
    pack=load(PACK_PATH); design=load(DESIGN_PATH)
    item=next(x for x in pack["content_items"] if x["id"]=="tpsi5-content-http-async-fetch-rest")
    assert pack["version"]=="0.10.0"
    assert item["path"]=="content/tpsi5/05_HTTP_ASYNC_FETCH_REST.md" and item["order"]==6
    assert item["activity_ids"]==[
        "tpsi5-activity-a-http-microscope-001","tpsi5-activity-b-async-response-policy-001",
        "tpsi5-activity-c-feisbuc-rest-client-001","tpsi5-activity-d-debug-fetch-http-001"]
    assert LESSON_PATH.is_file()
    uda23=next(u for u in design["years"][0]["udas"] if u["id"]=="uda-23")
    uda24=next(u for u in design["years"][0]["udas"] if u["id"]=="uda-24")
    assert len(uda23["items"])==1 and uda23["items"][0]["activity_ids"]==item["activity_ids"]
    assert [x["source"] for x in uda24["items"]]==[
        "content/tpsi5/06_NODE_EXPRESS_BACKEND.md",
        "content/tpsi5/07_SQL_RAW_PERSISTENCE.md",
        "content/tpsi5/08_AUTH_SESSIONI_SICUREZZA.md",
        "content/tpsi5/09_SSR_NUNJUCKS_CONFRONTO.md"]
    assert_activity(A_ROOT,"A","tpsi5-activity-a-http-microscope-001",False)
    b=assert_activity(B_ROOT,"B","tpsi5-activity-b-async-response-policy-001",True)
    c=assert_activity(C_ROOT,"C","tpsi5-activity-c-feisbuc-rest-client-001",False)
    assert_activity(D_ROOT,"D","tpsi5-activity-d-debug-fetch-http-001",False)
    assert b["linguaggio"]=="javascript" and c["project_milestone"]=="feisbuc-04-rest-api-client"


def test_async_response_policy_reference_passes_real_javascript_runner():
    activity=load(B_ROOT/"activity.json")
    report=grade_activity.grade_activity(activity,B_ROOT/"solution/main.js",timeout_seconds=5)
    assert report["passed"] is True,report


def test_http_microscope_fixture_exposes_status_header_and_method_semantics():
    with RunningServer(A_ROOT/"starter/server.mjs") as server:
        status,headers,posts=request(f"{server.base}/api/posts"); assert status==200 and headers.get_content_type()=="application/json" and len(posts)==2
        status,headers,created=request(f"{server.base}/api/posts",method="POST",payload={"text":"CI HTTP"},content_type="application/json")
        assert status==201 and headers["Location"]==f"/api/posts/{created['id']}"
        bad=urllib.request.Request(f"{server.base}/api/posts",data=b"x",headers={"Content-Type":"text/plain"},method="POST")
        with pytest.raises(urllib.error.HTTPError) as media:urllib.request.urlopen(bad,timeout=5)
        assert media.value.code==415
        delete=urllib.request.Request(f"{server.base}/api/posts",method="DELETE")
        with pytest.raises(urllib.error.HTTPError) as method_error:urllib.request.urlopen(delete,timeout=5)
        assert method_error.value.code==405


def test_feisbuc_rest_fixture_and_reference_adapter_keep_contract():
    with RunningServer(C_ROOT/"starter/server.mjs") as server:
        _,_,before=request(f"{server.base}/api/posts"); assert len(before)==2
        _,_,created=request(f"{server.base}/api/posts",method="POST",payload={"text":"Milestone CI"},content_type="application/json")
        _,_,updated=request(f"{server.base}/api/posts/{created['id']}",method="PATCH",payload={"liked":True},content_type="application/json")
        assert updated["liked"] is True and updated["likes"]==1
        api_source=(C_ROOT/"solution/api.js").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); (root/"api.mjs").write_text(api_source,encoding="utf-8")
            (root/"runner.mjs").write_text("import {createApi} from './api.mjs'; const api=createApi(process.argv[2]); const c=await api.createPost('adapter'); const u=await api.setLiked(c.id,true); console.log(JSON.stringify({text:c.text,liked:u.liked,likes:u.likes}));",encoding="utf-8")
            result=subprocess.run(["node","runner.mjs",server.base],cwd=root,capture_output=True,text=True,timeout=10)
            assert result.returncode==0,result.stderr
            assert json.loads(result.stdout)=={"text":"adapter","liked":True,"likes":1}


def test_fetch_debug_solution_keeps_error_taxonomy():
    broken=(D_ROOT/"starter/client.js").read_text(); fixed=(D_ROOT/"solution/client.js").read_text(); diagnosis=(D_ROOT/"solution/DIAGNOSI.md").read_text().lower()
    assert '"Content-Type": "text/plain"' in broken and "Network error" in broken
    assert "response.ok" in fixed and "JSON.stringify" in fixed and "response.status === 204" in fixed
    for concept in ("404","415","204","content-type","network"):assert concept in diagnosis
