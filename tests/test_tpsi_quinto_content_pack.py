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
        self.classes: set[str] = set()

    def handle_starttag(self, tag: str, attrs) -> None:
        self.tags.append(tag)
        for name, value in attrs:
            if name == "class" and value:
                self.classes.update(value.split())


def parse_html(path: Path) -> StructureParser:
    parser = StructureParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def test_native_content_pack_v1_is_valid_and_pinned() -> None:
    pack = load(PACK_PATH)
    assert pack["schema_version"] == "thebitlab.content-pack.v1"
    assert pack["version"] == "0.8.0"
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
        "06_NODE_EXPRESS_BACKEND.md",
        "07_SQL_RAW_PERSISTENCE.md",
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
    assert decisions == {
        "frontend_framework": "tbd",
        "node_orm": "tbd",
        "typescript_depth": "tbd",
        "python_mirror": "fastapi",
        "main_backend": "node-express",
    }


def test_external_specs_docs_and_licensed_material_are_references_not_sources() -> None:
    pack = load(PACK_PATH)
    refs = {item["id"]: item for item in pack["references"]}

    assert refs["tpsi5-ref-rfc9110"]["role"] == "specification"
    assert refs["tpsi5-ref-fetch"]["role"] == "specification"
    assert refs["tpsi5-ref-node"]["role"] == "technical-reference"
    assert refs["tpsi5-ref-express"]["role"] == "technical-reference"
    assert refs["tpsi5-ref-sqlite"]["role"] == "technical-reference"
    assert refs["tpsi5-ref-manning-css-depth"]["access"] == "licensed"
    assert refs["tpsi5-ref-pluralsight-javascript"]["access"] == "licensed"

    for ref_id in (
        "tpsi5-ref-lab5-legacy",
        "tpsi5-ref-lab6-legacy",
        "tpsi5-ref-lab7-legacy",
        "tpsi5-ref-lab8-legacy",
        "tpsi5-ref-lab9-legacy",
        "tpsi5-ref-lab10-legacy",
    ):
        assert refs[ref_id]["role"] == "teacher-reference"

    source_providers = {source["provider"] for source in pack["sources"]}
    for provider in ("manning", "pluralsight", "mdn", "whatwg", "nodejs", "expressjs", "sqlite"):
        assert provider not in source_providers


def test_content_items_are_ordered_and_linked_to_real_files() -> None:
    pack = load(PACK_PATH)
    items = pack["content_items"]
    assert [item["order"] for item in items] == list(range(1, 9))
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
        "tpsi5-content-node-express-backend",
        "tpsi5-content-sql-raw-persistence",
    } <= ids


def test_uda24_is_decomposed_without_changing_its_week_budget() -> None:
    design = load(DESIGN_PATH)
    uda24 = next(uda for uda in design["years"][0]["udas"] if uda["id"] == "uda-24")
    assert uda24["weeks"] == "7"
    assert [item["source"] for item in uda24["items"]] == [
        "content/tpsi5/06_NODE_EXPRESS_BACKEND.md",
        "content/tpsi5/07_SQL_RAW_PERSISTENCE.md",
    ]
    assert "SQL raw" in uda24["items"][0]["frame"]["next_step"]
    assert "auth" in uda24["items"][1]["frame"]["next_step"].lower()


def test_uda21_activity_contracts_and_assets_remain_valid() -> None:
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
        for asset in activity.get("assets", []):
            assert (root / asset["path"]).is_file(), asset
            if asset["visibility"] == "student":
                assert asset["type"] not in {"teacher_only", "hidden_test"}
                assert asset.get("target_path")

    assert SUPPORTED_LANGUAGES["html"] == "planned"
    assert SUPPORTED_LANGUAGES["sql"] == "implemented"


def test_uda21_reference_solutions_keep_semantics_css_and_bootstrap_mapping() -> None:
    html = parse_html(UDA21_ACTIVITY_ROOTS["B"] / "solution" / "index.html")
    assert html.tags.count("header") == 1
    assert html.tags.count("nav") == 1
    assert html.tags.count("main") == 1
    assert html.tags.count("article") == 2

    css = (UDA21_ACTIVITY_ROOTS["C"] / "solution" / "style.css").read_text(encoding="utf-8")
    assert "display: grid" in css
    assert "display: flex" in css
    assert "@media (min-width: 56rem)" in css
    assert "!important" not in css
    assert "float:" not in css

    bootstrap = parse_html(UDA21_ACTIVITY_ROOTS["E"] / "solution" / "index.html")
    for expected in ("container", "row", "col-lg-6", "navbar", "card", "btn"):
        assert expected in bootstrap.classes
    mapping = (UDA21_ACTIVITY_ROOTS["E"] / "solution" / "MAPPING.md").read_text(encoding="utf-8")
    assert "CSS nativo" in mapping
    assert "Bootstrap" in mapping
