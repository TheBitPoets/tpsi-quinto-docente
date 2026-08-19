from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import shutil

from scripts import grade_activity
from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content" / "tpsi5" / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content" / "tpsi5" / "04_JAVASCRIPT_DOM_BROWSER_APIS.md"

ACTIVITY_A_ROOT = ROOT / "activities" / "tpsi5" / "js_feed_pipeline_a"
ACTIVITY_B_ROOT = ROOT / "activities" / "tpsi5" / "js_post_refactor_b"
ACTIVITY_C_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_dynamic_c"
ACTIVITY_D_ROOT = ROOT / "activities" / "tpsi5" / "js_debug_d"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.attrs: dict[str, list[dict[str, str | None]]] = {}

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        self.tags.append(tag)
        self.attrs.setdefault(tag, []).append(dict(attrs))


def parse_html(path: Path) -> StructureParser:
    parser = StructureParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def assert_assets_exist_and_are_separated(root: Path, activity: dict) -> set[str]:
    student_targets: set[str] = set()

    for asset in activity["assets"]:
        path = root / asset["path"]
        assert path.is_file(), path

        if asset["visibility"] == "student":
            assert asset["type"] not in {"hidden_test", "teacher_only"}
            target = asset.get("target_path")
            assert isinstance(target, str) and target
            assert target not in student_targets
            student_targets.add(target)
        else:
            assert asset["visibility"] == "teacher"

    return student_targets


def test_javascript_module_is_linked_to_pack_with_expected_provenance() -> None:
    pack = load(PACK_PATH)
    item = next(
        item
        for item in pack["content_items"]
        if item["id"] == "tpsi5-content-javascript-dom-browser"
    )

    assert item["path"] == "content/tpsi5/04_JAVASCRIPT_DOM_BROWSER_APIS.md"
    assert item["order"] == 5
    assert item["activity_ids"] == [
        "tpsi5-activity-a-js-feed-pipeline-001",
        "tpsi5-activity-b-js-post-refactor-001",
        "tpsi5-activity-c-feisbuc-dynamic-feed-001",
        "tpsi5-activity-d-debug-feisbuc-js-001",
    ]
    refs = {ref["id"] for ref in item["source_refs"]}
    assert {
        "tpsi5-source-originali",
        "tpsi5-source-labs-legacy",
        "tpsi5-source-feisbuc-legacy",
        "tpsi5-ref-lab3-legacy",
        "tpsi5-ref-mdn",
        "tpsi5-ref-ecmascript",
        "tpsi5-ref-pluralsight-javascript",
    } <= refs
    assert LESSON_PATH.is_file()


def test_uda22_schedules_module_and_keeps_async_http_for_next_uda() -> None:
    design = load(DESIGN_PATH)
    year = design["years"][0]
    uda22 = next(uda for uda in year["udas"] if uda["id"] == "uda-22")
    uda23 = next(uda for uda in year["udas"] if uda["id"] == "uda-23")

    assert len(uda22["items"]) == 1
    item = uda22["items"][0]
    assert item["source"] == "content/tpsi5/04_JAVASCRIPT_DOM_BROWSER_APIS.md"
    assert item["activity_ids"] == [
        "tpsi5-activity-a-js-feed-pipeline-001",
        "tpsi5-activity-b-js-post-refactor-001",
        "tpsi5-activity-c-feisbuc-dynamic-feed-001",
        "tpsi5-activity-d-debug-feisbuc-js-001",
    ]
    assert item["frame"]["status"] == "draft"
    assert "HTTP" in item["frame"]["next_step"]
    assert "async" in item["frame"]["next_step"]
    assert uda23["title"] == "HTTP, asincronia, Fetch e REST"
    assert uda23["items"] == []


def test_uda22_activity_contracts_assets_and_grading_boundary() -> None:
    pack = load(PACK_PATH)
    known_content_ids = {item["id"] for item in pack["content_items"]}
    expected = [
        (
            ACTIVITY_A_ROOT,
            "A",
            "tpsi5-activity-a-js-feed-pipeline-001",
            {"main.js", "README.md"},
            True,
        ),
        (
            ACTIVITY_B_ROOT,
            "B",
            "tpsi5-activity-b-js-post-refactor-001",
            {"main.js", "README.md"},
            True,
        ),
        (
            ACTIVITY_C_ROOT,
            "C",
            "tpsi5-activity-c-feisbuc-dynamic-feed-001",
            {"index.html", "custom.css", "app.js", "posts.js", "storage.js", "README.md"},
            False,
        ),
        (
            ACTIVITY_D_ROOT,
            "D",
            "tpsi5-activity-d-debug-feisbuc-js-001",
            {"index.html", "app.js", "DIAGNOSI.md", "README.md"},
            False,
        ),
    ]

    for root, difficulty, activity_id, targets, automatic in expected:
        path = root / "activity.json"
        activity = load(path)
        assert validate_activity(activity, str(path)) == []
        assert activity["id"] == activity_id
        assert activity["difficolta"] == difficulty
        assert activity["linguaggio"] == "javascript"
        assert set(activity["content_ids"]) <= known_content_ids
        assert sum(item["punti"] for item in activity["rubrica"]) == 10
        assert assert_assets_exist_and_are_separated(root, activity) == targets

        if automatic:
            assert activity["correzione"]["test"] is True
            assert activity["correzione"]["sandbox"] is True
            assert activity["test_cases"]
        else:
            assert activity["correzione"] == {
                "compila": False,
                "test": False,
                "sandbox": False,
                "ai_feedback": False,
            }


def test_platform_javascript_runner_is_implemented_but_browser_runtime_is_not_claimed() -> None:
    assert grade_activity.SUPPORTED_LANGUAGES["javascript"] == "implemented"
    assert grade_activity.SUPPORTED_LANGUAGES["nodejs"] == "implemented"
    assert grade_activity.SUPPORTED_LANGUAGES["html"] == "planned"

    assert load(ACTIVITY_A_ROOT / "activity.json")["correzione"]["test"] is True
    assert load(ACTIVITY_B_ROOT / "activity.json")["correzione"]["test"] is True
    assert load(ACTIVITY_C_ROOT / "activity.json")["correzione"]["test"] is False
    assert load(ACTIVITY_D_ROOT / "activity.json")["correzione"]["test"] is False


def test_autograded_javascript_reference_solutions_pass_real_platform_runner() -> None:
    assert shutil.which("node") is not None, "Node.js richiesto dalla CI TPSI5"

    for root in (ACTIVITY_A_ROOT, ACTIVITY_B_ROOT):
        activity = load(root / "activity.json")
        report = grade_activity.grade_activity(
            activity,
            root / "solution" / "main.js",
            timeout_seconds=5,
        )
        assert report["passed"] is True, report
        assert report["status"] == "passed"
        assert report["language"] == "javascript"
        assert report["summary"] == {
            "passed": len(activity["test_cases"]),
            "total": len(activity["test_cases"]),
        }


def test_activity_a_and_b_solutions_express_intended_data_patterns() -> None:
    pipeline = (ACTIVITY_A_ROOT / "solution" / "main.js").read_text(encoding="utf-8")
    state = (ACTIVITY_B_ROOT / "solution" / "main.js").read_text(encoding="utf-8")

    assert ".filter(" in pipeline
    assert ".map(" in pipeline
    assert ".trim()" in pipeline
    assert "popular: likes >= 5" in pipeline

    assert ".map(" in state
    assert "...post" in state
    assert "Math.max(0" in state
    assert "post.id !== targetId" in state


def test_dynamic_feisbuc_starter_exposes_semantic_browser_contract() -> None:
    parser = parse_html(ACTIVITY_C_ROOT / "starter" / "index.html")
    html = (ACTIVITY_C_ROOT / "starter" / "index.html").read_text(encoding="utf-8")

    assert parser.tags.count("form") == 1
    assert parser.tags.count("textarea") == 1
    assert parser.tags.count("section") >= 2
    assert 'id="composer-form"' in html
    assert 'id="post-list"' in html
    assert 'aria-live="polite"' in html
    assert 'type="module" src="app.js"' in html
    assert "bootstrap@5.3.8" in html


def test_dynamic_feisbuc_reference_implements_state_render_delegation_and_storage() -> None:
    app = (ACTIVITY_C_ROOT / "solution" / "app.js").read_text(encoding="utf-8")
    posts = (ACTIVITY_C_ROOT / "solution" / "posts.js").read_text(encoding="utf-8")
    storage = (ACTIVITY_C_ROOT / "solution" / "storage.js").read_text(encoding="utf-8")

    for fragment in (
        'addEventListener("submit"',
        "event.preventDefault()",
        "new FormData(form)",
        'postList.addEventListener("click"',
        ".closest(",
        "dataset.postId",
        "textContent",
        "replaceChildren",
        "commitPosts",
    ):
        assert fragment in app

    assert "crypto.randomUUID()" in posts
    assert ".map(" in posts
    assert "...post" in posts

    assert "localStorage.setItem" in storage
    assert "localStorage.getItem" in storage
    assert "JSON.stringify" in storage
    assert "JSON.parse" in storage
    assert "try" in storage and "catch" in storage
    assert "Array.isArray" in storage

    combined = "\n".join((app, posts, storage))
    assert "fetch(" not in combined
    assert "async " not in combined
    assert "Promise" not in combined
    assert "innerHTML" not in combined


def test_debug_activity_contains_real_faults_and_reference_removes_them() -> None:
    broken = (ACTIVITY_D_ROOT / "starter" / "app.js").read_text(encoding="utf-8")
    fixed = (ACTIVITY_D_ROOT / "solution" / "app.js").read_text(encoding="utf-8")
    diagnosis = (ACTIVITY_D_ROOT / "solution" / "DIAGNOSI.md").read_text(encoding="utf-8")

    assert 'addEventListener("submit", (e)' in broken
    assert "event.preventDefault()" in broken
    assert 'localStorage.setItem(STORAGE_KEY, { text:' in broken
    assert 'querySelectorAll(".like-button")' in broken
    assert ".forEach((button)" in broken
    assert "let counter = 0" in broken
    assert ".innerHTML = text" in broken

    assert 'addEventListener("submit", (event)' in fixed
    assert 'feed.addEventListener("click"' in fixed
    assert "data-post-id" not in fixed  # dataset API produces the attribute at runtime
    assert "dataset.postId" in fixed
    assert "dataset.action" in fixed
    assert "JSON.stringify(posts)" in fixed
    assert "JSON.parse(raw)" in fixed
    assert ".textContent = post.text" in fixed
    assert "querySelectorAll" not in fixed
    assert "let counter" not in fixed
    assert "innerHTML" not in fixed
    assert "fetch(" not in fixed

    for concept in (
        "event.preventDefault",
        "JSON.parse",
        "event delegation",
        "data-post-id",
        "textContent",
        "state",
    ):
        assert concept.lower() in diagnosis.lower()


def test_legacy_audit_records_javascript_migration_and_async_deferral() -> None:
    audit = (ROOT / "doc" / "LEGACY_REUSE_AUDIT.md").read_text(encoding="utf-8")

    assert "0deae0eb606bc9c2849ba271bdf03c128910f1ac" in audit
    assert "Promise, `async`/`await` e `fetch`" in audit
    assert "event.preventDefault()" in audit
    assert "event delegation" in audit.lower()
    assert "data-post-id" in audit
    assert "feisbuc-03-dynamic-local-feed" in audit
