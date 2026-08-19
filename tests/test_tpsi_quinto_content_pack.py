from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path

from scripts import course_source_catalog
from scripts.content_pack_contract import project_course_design_sources, validate_content_pack
from scripts.grade_activity import SUPPORTED_LANGUAGES
from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content" / "tpsi5" / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quinto_2026_2027.json"
ACCEPTED_CONTENT_PACK_V1_SHA = "5472eef86568a4e7ce59ad34ba937220df27efd7"

UDA21_ACTIVITY_ROOTS = {
    "A": ROOT / "activities" / "tpsi5" / "html_anatomy_a",
    "B": ROOT / "activities" / "tpsi5" / "feisbuc_semantic_b",
    "C": ROOT / "activities" / "tpsi5" / "feisbuc_responsive_c",
    "D": ROOT / "activities" / "tpsi5" / "css_debug_d",
    "E": ROOT / "activities" / "tpsi5" / "feisbuc_bootstrap_e",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.attrs: dict[str, list[dict[str, str | None]]] = {}
        self.declarations: list[str] = []

    def handle_decl(self, decl: str) -> None:
        self.declarations.append(decl.lower())

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        self.attrs.setdefault(tag, []).append(dict(attrs))


def parse_html(path: Path) -> StructureParser:
    parser = StructureParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def all_classes(parser: StructureParser) -> set[str]:
    result: set[str] = set()
    for entries in parser.attrs.values():
        for attrs in entries:
            value = attrs.get("class")
            if value:
                result.update(value.split())
    return result


def test_native_content_pack_v1_is_valid_and_pinned() -> None:
    pack = load(PACK_PATH)
    assert pack["schema_version"] == "thebitlab.content-pack.v1"
    assert pack["version"] == "0.6.0"
    assert pack["status"] == "draft"
    assert pack["extensions"]["platform_contract"]["content_pack_v1_sha"] == ACCEPTED_CONTENT_PACK_V1_SHA
    assert validate_content_pack(pack, str(PACK_PATH), root=ROOT) == []


def test_sources_project_exactly_to_course_design_catalog() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    projected = project_course_design_sources(pack)
    assert design["sources"] == projected

    normalized = course_source_catalog.normalize_course_sources({"sources": projected})
    assert [source.source_id for source in normalized] == [
        "tpsi5-source-originali",
        "tpsi5-source-html-css-legacy",
        "tpsi5-source-labs-legacy",
        "tpsi5-source-feisbuc-legacy",
    ]
    assert normalized[0].files == (
        "README.md",
        "COVERAGE.md",
        "00_COURSE_ARCHITECTURE.md",
        "01_WEB_PLATFORM_HTML_MODERNO.md",
        "02_CSS_MODERNO_RESPONSIVE.md",
        "03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md",
        "04_JAVASCRIPT_DOM_BROWSER_APIS.md",
        "05_HTTP_ASYNC_FETCH_REST.md",
    )
    assert normalized[1].ref == "d71da420f1aa2ea39b61356e4f9900c6371e7a42"
    assert normalized[2].ref == "36a909f00c9478983a8d1b950440e2abc28b8a55"
    assert normalized[3].ref == "086995ece4260a3408740b94cfe2701ce24f8b57"


def test_course_design_keeps_33_week_draft_and_open_decisions() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    year = design["years"][0]

    assert year["weeks"] == 33
    assert sum(int(uda["weeks"]) for uda in year["udas"]) == 33
    assert [uda["id"] for uda in year["udas"]] == [
        "uda-20", "uda-21", "uda-22", "uda-23", "uda-24", "uda-25", "uda-26"
    ]

    decisions = pack["extensions"]["bootstrap_decisions"]
    assert decisions["frontend_framework"] == "tbd"
    assert decisions["node_orm"] == "tbd"
    assert decisions["typescript_depth"] == "tbd"
    assert decisions["main_backend"] == "node-express"
    assert decisions["python_mirror"] == "fastapi"


def test_public_specs_and_licensed_teacher_references_are_not_sources() -> None:
    pack = load(PACK_PATH)
    refs = {item["id"]: item for item in pack["references"]}

    assert refs["tpsi5-ref-mdn"]["role"] == "technical-reference"
    assert refs["tpsi5-ref-rfc9110"]["role"] == "specification"
    assert refs["tpsi5-ref-fetch"]["role"] == "specification"
    assert refs["tpsi5-ref-ecmascript"]["role"] == "specification"
    assert refs["tpsi5-ref-manning-css-depth"]["access"] == "licensed"
    assert refs["tpsi5-ref-pluralsight-javascript"]["access"] == "licensed"
    assert refs["tpsi5-ref-lab5-legacy"]["role"] == "teacher-reference"
    assert refs["tpsi5-ref-lab6-legacy"]["role"] == "teacher-reference"
    assert refs["tpsi5-ref-lab7-legacy"]["role"] == "teacher-reference"

    providers = {source["provider"] for source in pack["sources"]}
    assert "manning" not in providers
    assert "pluralsight" not in providers
    assert "mdn" not in providers
    assert "whatwg" not in providers


def test_content_items_are_ordered_and_linked_to_real_files() -> None:
    pack = load(PACK_PATH)
    items = pack["content_items"]
    assert [item["order"] for item in items] == list(range(1, 7))
    for item in items:
        assert (ROOT / item["path"]).is_file(), item["path"]
        assert item["source_refs"]

    ids = {item["id"] for item in items}
    assert {
        "tpsi5-content-web-platform-html",
        "tpsi5-content-css-modern-responsive",
        "tpsi5-content-bootstrap-framework",
        "tpsi5-content-javascript-dom-browser",
        "tpsi5-content-http-async-fetch-rest",
    } <= ids


def test_uda21_activity_contracts_and_student_teacher_assets_remain_valid() -> None:
    known_content_ids = {item["id"] for item in load(PACK_PATH)["content_items"]}
    expected_ids = {
        "A": "tpsi5-activity-a-html-anatomy-001",
        "B": "tpsi5-activity-b-feisbuc-semantic-001",
        "C": "tpsi5-activity-c-feisbuc-responsive-layout-001",
        "D": "tpsi5-activity-d-debug-responsive-css-001",
        "E": "tpsi5-activity-e-feisbuc-bootstrap-ui-001",
    }

    for difficulty, root in UDA21_ACTIVITY_ROOTS.items():
        activity = load(root / "activity.json")
        assert validate_activity(activity, str(root / "activity.json")) == []
        assert activity["id"] == expected_ids[difficulty]
        assert activity["difficolta"] == difficulty
        assert set(activity.get("content_ids", [])) <= known_content_ids
        assert sum(entry["punti"] for entry in activity["rubrica"]) == 10

        student_targets: set[str] = set()
        for asset in activity["assets"]:
            assert (root / asset["path"]).is_file(), asset
            if asset["visibility"] == "student":
                assert asset["type"] not in {"teacher_only", "hidden_test"}
                target = asset.get("target_path")
                assert isinstance(target, str) and target
                assert target not in student_targets
                student_targets.add(target)
            else:
                assert asset["visibility"] == "teacher"


def test_uda21_reference_solutions_keep_semantics_and_modern_layout() -> None:
    html_a = parse_html(UDA21_ACTIVITY_ROOTS["A"] / "solution" / "index.html")
    assert "doctype html" in html_a.declarations
    assert html_a.attrs["html"][0].get("lang") == "it"
    assert html_a.tags.count("main") == 1
    assert html_a.tags.count("h1") == 1

    semantic = parse_html(UDA21_ACTIVITY_ROOTS["B"] / "solution" / "index.html")
    for tag in ("header", "nav", "main", "article", "footer"):
        assert tag in semantic.tags

    css = (UDA21_ACTIVITY_ROOTS["C"] / "solution" / "style.css").read_text(encoding="utf-8")
    assert "display: grid" in css
    assert "display: flex" in css
    assert "@media" in css
    assert "!important" not in css

    broken = (UDA21_ACTIVITY_ROOTS["D"] / "starter" / "style.css").read_text(encoding="utf-8")
    fixed = (UDA21_ACTIVITY_ROOTS["D"] / "solution" / "style.css").read_text(encoding="utf-8")
    assert "box-sizing: content-box" in broken
    assert "!important" in broken
    assert "box-sizing: border-box" in fixed
    assert "!important" not in fixed

    bootstrap_html = (UDA21_ACTIVITY_ROOTS["E"] / "solution" / "index.html").read_text(encoding="utf-8")
    bootstrap_css = (UDA21_ACTIVITY_ROOTS["E"] / "solution" / "custom.css").read_text(encoding="utf-8")
    parsed = parse_html(UDA21_ACTIVITY_ROOTS["E"] / "solution" / "index.html")
    classes = all_classes(parsed)
    assert "bootstrap@5.3.8" in bootstrap_html
    assert {"container", "row", "col-12", "navbar", "card", "btn"} <= classes
    assert "display: grid" not in bootstrap_css
    assert "@media" not in bootstrap_css


def test_grading_boundary_still_matches_platform_contract() -> None:
    assert SUPPORTED_LANGUAGES["javascript"] == "implemented"
    assert SUPPORTED_LANGUAGES["nodejs"] == "implemented"
    assert SUPPORTED_LANGUAGES["html"] == "planned"
