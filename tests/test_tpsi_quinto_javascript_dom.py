from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import shutil

from scripts import grade_activity
from scripts.validate_activity import validate_activity

ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content/tpsi5/content-pack.json"
DESIGN_PATH = ROOT / "doc/course_designs/tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content/tpsi5/04_JAVASCRIPT_DOM_BROWSER_APIS.md"
A_ROOT = ROOT / "activities/tpsi5/js_feed_pipeline_a"
B_ROOT = ROOT / "activities/tpsi5/js_post_refactor_b"
C_ROOT = ROOT / "activities/tpsi5/feisbuc_dynamic_c"
D_ROOT = ROOT / "activities/tpsi5/js_debug_d"


def load(path: Path) -> dict:
    value=json.loads(path.read_text(encoding="utf-8")); assert isinstance(value,dict); return value


class StructureParser(HTMLParser):
    def __init__(self): super().__init__(); self.tags=[]
    def handle_starttag(self,tag,attrs): self.tags.append(tag)


def parse_html(path):
    parser=StructureParser(); parser.feed(path.read_text(encoding="utf-8")); return parser


def assert_assets(root,activity):
    targets=set()
    for asset in activity["assets"]:
        assert (root/asset["path"]).is_file(),asset
        if asset["visibility"]=="student":
            target=asset.get("target_path"); assert isinstance(target,str) and target and target not in targets; targets.add(target)
        else: assert asset["visibility"]=="teacher"
    return targets


def test_javascript_module_provenance_and_course_design_continuity():
    pack=load(PACK_PATH); item=next(x for x in pack["content_items"] if x["id"]=="tpsi5-content-javascript-dom-browser")
    assert item["path"]=="content/tpsi5/04_JAVASCRIPT_DOM_BROWSER_APIS.md" and item["order"]==5
    assert item["activity_ids"]==["tpsi5-activity-a-js-feed-pipeline-001","tpsi5-activity-b-js-post-refactor-001","tpsi5-activity-c-feisbuc-dynamic-feed-001","tpsi5-activity-d-debug-feisbuc-js-001"]
    assert {"tpsi5-source-originali","tpsi5-source-labs-legacy","tpsi5-source-feisbuc-legacy","tpsi5-ref-lab3-legacy","tpsi5-ref-mdn","tpsi5-ref-ecmascript","tpsi5-ref-pluralsight-javascript"} <= {r["id"] for r in item["source_refs"]}
    assert LESSON_PATH.is_file()
    design=load(DESIGN_PATH); year=design["years"][0]
    uda22=next(u for u in year["udas"] if u["id"]=="uda-22"); uda23=next(u for u in year["udas"] if u["id"]=="uda-23")
    assert len(uda22["items"])==1 and uda22["items"][0]["source"]=="content/tpsi5/04_JAVASCRIPT_DOM_BROWSER_APIS.md"
    assert "HTTP" in uda22["items"][0]["frame"]["next_step"]
    assert len(uda23["items"])==1 and uda23["items"][0]["source"]=="content/tpsi5/05_HTTP_ASYNC_FETCH_REST.md"


def test_uda22_activity_contracts_assets_and_grading_boundary():
    known={x["id"] for x in load(PACK_PATH)["content_items"]}
    expected=[
        (A_ROOT,"A","tpsi5-activity-a-js-feed-pipeline-001",{"main.js","README.md"},True),
        (B_ROOT,"B","tpsi5-activity-b-js-post-refactor-001",{"main.js","README.md"},True),
        (C_ROOT,"C","tpsi5-activity-c-feisbuc-dynamic-feed-001",{"index.html","custom.css","app.js","posts.js","storage.js","README.md"},False),
        (D_ROOT,"D","tpsi5-activity-d-debug-feisbuc-js-001",{"index.html","app.js","DIAGNOSI.md","README.md"},False)]
    for root,difficulty,activity_id,targets,automatic in expected:
        activity=load(root/"activity.json"); assert validate_activity(activity,str(root/"activity.json"))==[]
        assert activity["id"]==activity_id and activity["difficolta"]==difficulty and activity["linguaggio"]=="javascript"
        assert set(activity["content_ids"])<=known and sum(x["punti"] for x in activity["rubrica"])==10
        assert assert_assets(root,activity)==targets
        assert activity["correzione"]["test"] is automatic and activity["correzione"]["sandbox"] is automatic


def test_autograded_uda22_reference_solutions_pass_real_platform_runner():
    assert shutil.which("node") is not None
    for root in (A_ROOT,B_ROOT):
        activity=load(root/"activity.json"); report=grade_activity.grade_activity(activity,root/"solution/main.js",timeout_seconds=5)
        assert report["passed"] is True,report


def test_pure_javascript_patterns_remain_intentional():
    pipeline=(A_ROOT/"solution/main.js").read_text(); state=(B_ROOT/"solution/main.js").read_text()
    assert ".filter(" in pipeline and ".map(" in pipeline and ".trim()" in pipeline
    assert ".map(" in state and "...post" in state and "Math.max(0" in state


def test_dynamic_feisbuc_starter_and_reference_keep_state_render_boundary():
    html=(C_ROOT/"starter/index.html").read_text(); parser=parse_html(C_ROOT/"starter/index.html")
    app=(C_ROOT/"solution/app.js").read_text(); posts=(C_ROOT/"solution/posts.js").read_text(); storage=(C_ROOT/"solution/storage.js").read_text()
    assert parser.tags.count("form")==1 and 'id="composer-form"' in html and 'id="post-list"' in html and 'aria-live="polite"' in html and 'type="module" src="app.js"' in html
    for fragment in ('addEventListener("submit"',"event.preventDefault()","new FormData(form)",'postList.addEventListener("click"',"dataset.postId","textContent","replaceChildren","commitPosts"): assert fragment in app
    assert "crypto.randomUUID()" in posts and ".map(" in posts
    assert "localStorage.setItem" in storage and "localStorage.getItem" in storage and "JSON.stringify" in storage and "JSON.parse" in storage
    assert "fetch(" not in "\n".join((app,posts,storage))


def test_debug_activity_preserves_real_legacy_faults_and_reference_removes_them():
    broken=(D_ROOT/"starter/app.js").read_text(); fixed=(D_ROOT/"solution/app.js").read_text(); diagnosis=(D_ROOT/"solution/DIAGNOSI.md").read_text()
    assert "event.preventDefault()" in broken and 'localStorage.setItem(STORAGE_KEY, { text:' in broken and 'querySelectorAll(".like-button")' in broken and "let counter = 0" in broken and ".innerHTML = text" in broken
    assert 'feed.addEventListener("click"' in fixed and "dataset.postId" in fixed and "JSON.stringify(posts)" in fixed and "JSON.parse(raw)" in fixed and ".textContent = post.text" in fixed
    assert "querySelectorAll" not in fixed and "let counter" not in fixed and "innerHTML" not in fixed
    for concept in ("event.preventDefault","JSON.parse","event delegation","data-post-id","textContent","state"): assert concept.lower() in diagnosis.lower()


def test_legacy_audit_keeps_async_move_to_uda23_visible():
    audit=(ROOT/"doc/LEGACY_REUSE_AUDIT.md").read_text(encoding="utf-8")
    assert "0deae0eb606bc9c2849ba271bdf03c128910f1ac" in audit
    assert "Promise/async-await" in audit or "Promise, `async`/`await`" in audit
    assert "UDA 23" in audit or "UDA23" in audit
    assert "event delegation" in audit.lower()
    assert "feisbuc-03-dynamic-local-feed" in audit or "milestone 3" in audit
