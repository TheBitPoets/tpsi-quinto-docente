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
    assert pack["version"] == "0.5.0"
    assert pack["status"] == "draft"
    assert (
        pack["extensions"]["platform_contract"]["content_pack_v1_sha"]
        == ACCEPTED_CONTENT_PACK_V1_SHA
    )
    assert validate_content_pack(pack, str(PACK_PATH), root=ROOT) == []


def test_pack_sources_project_to_current_course_source_catalog() -> None:
    pack = load(PACK_PATH)
    projected = project_course_design_sources(pack)
    normalized = course_source_catalog.normalize_course_sources({"sources": projected})

    assert [source.source_id for source in normalized] == [
        "tpsi5-source-originali",
        "tpsi5-source-html-css-legacy",
        "tpsi5-source-labs-legacy",
        "tpsi5-source-feisbuc-legacy",
    ]
    assert [source.provider for source in normalized] == [
        "local",
        "github",
        "github",
        "github",
    ]
    assert normalized[0].path == "content/tpsi5"
    assert normalized[0].files == (
        "README.md",
        "COVERAGE.md",
        "00_COURSE_ARCHITECTURE.md",
        "01_WEB_PLATFORM_HTML_MODERNO.md",
        "02_CSS_MODERNO_RESPONSIVE.md",
        "03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md",
        "04_JAVASCRIPT_DOM_BROWSER_APIS.md",
    )
    assert normalized[1].ref == "d71da420f1aa2ea39b61356e4f9900c6371e7a42"
    assert normalized[2].ref == "36a909f00c9478983a8d1b950440e2abc28b8a55"
    assert normalized[3].ref == "086995ece4260a3408740b94cfe2701ce24f8b57"


def test_course_design_uses_exact_content_pack_source_projection() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)
    assert design["sources"] == project_course_design_sources(pack)


def test_course_design_keeps_33_weeks_and_open_decisions() -> None:
    design = load(DESIGN_PATH)
    year = design["years"][0]
    pack = load(PACK_PATH)
    decisions = pack["extensions"]["bootstrap_decisions"]

    assert year["weeks"] == 33
    assert sum(int(uda["weeks"]) for uda in year["udas"]) == 33
    assert [uda["id"] for uda in year["udas"]] == [
        "uda-20",
        "uda-21",
        "uda-22",
        "uda-23",
        "uda-24",
        "uda-25",
        "uda-26",
    ]
    assert decisions["frontend_framework"] == "tbd"
    assert decisions["node_orm"] == "tbd"
    assert decisions["typescript_depth"] == "tbd"
    assert decisions["main_backend"] == "node-express"
    assert decisions["python_mirror"] == "fastapi"


def test_references_keep_public_specs_and_licensed_material_separate() -> None:
    pack = load(PACK_PATH)
    refs = {item["id"]: item for item in pack["references"]}

    assert refs["tpsi5-ref-mdn"]["role"] == "technical-reference"
    assert refs["tpsi5-ref-ecmascript"]["role"] == "specification"
    assert refs["tpsi5-ref-whatwg-html"]["role"] == "specification"
    assert refs["tpsi5-ref-rfc9110"]["role"] == "specification"
    assert refs["tpsi5-ref-manning-css-depth"]["access"] == "licensed"
    assert refs["tpsi5-ref-pluralsight-javascript"]["access"] == "licensed"
    assert refs["tpsi5-ref-lab3-legacy"]["role"] == "teacher-reference"

    source_providers = {source["provider"] for source in pack["sources"]}
    assert "mdn" not in source_providers
    assert "manning" not in source_providers
    assert "pluralsight" not in source_providers
    assert "tc39" not in source_providers


def test_content_items_are_ordered_and_files_exist() -> None:
    pack = load(PACK_PATH)
    items = pack["content_items"]

    assert [item["order"] for item in items] == [1, 2, 3, 4, 5]
    assert [item["id"] for item in items] == [
        "tpsi5-content-course-architecture",
        "tpsi5-content-web-platform-html",
        "tpsi5-content-css-modern-responsive",
        "tpsi5-content-bootstrap-framework",
        "tpsi5-content-javascript-dom-browser",
    ]
    for item in items:
        assert (ROOT / item["path"]).is_file()
        assert item["source_refs"]


def test_uda21_keeps_html_css_bootstrap_progression() -> None:
    design = load(DESIGN_PATH)
    uda21 = next(uda for uda in design["years"][0]["udas"] if uda["id"] == "uda-21")

    assert [item["source"] for item in uda21["items"]] == [
        "content/tpsi5/01_WEB_PLATFORM_HTML_MODERNO.md",
        "content/tpsi5/02_CSS_MODERNO_RESPONSIVE.md",
        "content/tpsi5/03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md",
    ]
    assert all(item["frame"]["status"] == "draft" for item in uda21["items"])


def test_uda21_activity_contracts_and_student_teacher_separation() -> None:
    pack = load(PACK_PATH)
    known_content_ids = {item["id"] for item in pack["content_items"]}

    for difficulty, root in UDA21_ACTIVITY_ROOTS.items():
        path = root / "activity.json"
        activity = load(path)
        assert validate_activity(activity, str(path)) == []
        assert activity["difficolta"] == difficulty
        assert set(activity.get("content_ids", [])) <= known_content_ids
        assert sum(item["punti"] for item in activity["rubrica"]) == 10
        assert activity["correzione"]["test"] is False

        student_targets: set[str] = set()
        for asset in activity["assets"]:
            asset_path = root / asset["path"]
            assert asset_path.is_file(), asset_path
            if asset["visibility"] == "student":
                assert asset["type"] not in {"hidden_test", "teacher_only"}
                target = asset.get("target_path")
                assert isinstance(target, str) and target
                assert target not in student_targets
                student_targets.add(target)
            else:
                assert asset["visibility"] == "teacher"


def test_html_browser_auto_grading_is_still_not_claimed() -> None:
    assert SUPPORTED_LANGUAGES["html"] == "planned"
    for root in UDA21_ACTIVITY_ROOTS.values():
        assert load(root / "activity.json")["correzione"]["test"] is False


def test_html_semantic_reference_solution_remains_valid() -> None:
    solution = parse_html(UDA21_ACTIVITY_ROOTS["B"] / "solution" / "index.html")

    assert solution.tags.count("header") == 1
    assert solution.tags.count("nav") == 1
    assert solution.tags.count("main") == 1
    assert solution.tags.count("article") == 2
    assert solution.tags.count("footer") == 1


def test_css_reference_solution_uses_modern_layout_and_debug_fix_removes_faults() -> None:
    responsive = (UDA21_ACTIVITY_ROOTS["C"] / "solution" / "style.css").read_text(
        encoding="utf-8"
    )
    broken = (UDA21_ACTIVITY_ROOTS["D"] / "starter" / "style.css").read_text(
        encoding="utf-8"
    )
    fixed = (UDA21_ACTIVITY_ROOTS["D"] / "solution" / "style.css").read_text(
        encoding="utf-8"
    )

    assert "display: grid" in responsive
    assert "display: flex" in responsive
    assert "@media (min-width: 56rem)" in responsive
    assert "float:" not in responsive
    assert "!important" not in responsive

    assert "width: 1200px" in broken
    assert "!important" in broken
    assert "flex-wrap: nowrap" in broken
    assert "width: 1200px" not in fixed
    assert "!important" not in fixed
    assert "flex-wrap: wrap" in fixed


def test_bootstrap_reference_solution_preserves_semantics_and_minimal_custom_css() -> None:
    root = UDA21_ACTIVITY_ROOTS["E"]
    html = (root / "solution" / "index.html").read_text(encoding="utf-8")
    css = (root / "solution" / "custom.css").read_text(encoding="utf-8")
    parsed = parse_html(root / "solution" / "index.html")
    classes = all_classes(parsed)

    assert "bootstrap@5.3.8/dist/css/bootstrap.min.css" in html
    assert "bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" in html
    for name in ("container", "row", "col-12", "col-lg-3", "col-lg-6", "card"):
        assert name in classes
    assert parsed.tags.count("article") == 2
    assert "display: grid" not in css
    assert "display: flex" not in css
    assert "@media" not in css
    assert "!important" not in css


def test_legacy_audit_preserves_previous_migration_evidence() -> None:
    audit = (ROOT / "doc" / "LEGACY_REUSE_AUDIT.md").read_text(encoding="utf-8")

    assert "`Scheletro html` | **rewrite**" in audit
    assert "`CSS sintassi` | **migrated/rewrite**" in audit
    assert "`Box Model` | **migrated/major update**" in audit
    assert "feisbuc-00-semantic-skeleton" in audit
    assert "feisbuc-01-responsive-shell" in audit
    assert "feisbuc-03-dynamic-local-feed" in audit
