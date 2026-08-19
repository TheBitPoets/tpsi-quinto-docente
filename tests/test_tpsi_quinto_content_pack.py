from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path

from scripts import course_source_catalog
from scripts.content_pack_contract import (
    project_course_design_sources,
    validate_content_pack,
)
from scripts.grade_activity import SUPPORTED_LANGUAGES
from scripts.validate_activity import validate_activity


ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content" / "tpsi5" / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quinto_2026_2027.json"
HTML_LESSON_PATH = ROOT / "content" / "tpsi5" / "01_WEB_PLATFORM_HTML_MODERNO.md"
CSS_LESSON_PATH = ROOT / "content" / "tpsi5" / "02_CSS_MODERNO_RESPONSIVE.md"
BOOTSTRAP_LESSON_PATH = ROOT / "content" / "tpsi5" / "03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md"
ACTIVITY_A_ROOT = ROOT / "activities" / "tpsi5" / "html_anatomy_a"
ACTIVITY_B_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_semantic_b"
ACTIVITY_C_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_responsive_c"
ACTIVITY_D_ROOT = ROOT / "activities" / "tpsi5" / "css_debug_d"
ACTIVITY_E_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_bootstrap_e"
ACCEPTED_CONTENT_PACK_V1_SHA = "5472eef86568a4e7ce59ad34ba937220df27efd7"


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


def classes(parser: StructureParser) -> set[str]:
    result: set[str] = set()
    for entries in parser.attrs.values():
        for attrs in entries:
            value = attrs.get("class")
            if value:
                result.update(value.split())
    return result


def test_native_content_pack_v1_is_valid() -> None:
    pack = load(PACK_PATH)

    assert pack["schema_version"] == "thebitlab.content-pack.v1"
    assert pack["version"] == "0.4.1"
    assert pack["status"] == "draft"
    assert (
        pack["extensions"]["platform_contract"]["content_pack_v1_sha"]
        == ACCEPTED_CONTENT_PACK_V1_SHA
    )
    assert validate_content_pack(pack, str(PACK_PATH), root=ROOT) == []


def test_pack_sources_project_to_current_course_source_catalog() -> None:
    pack = load(PACK_PATH)
    projected = project_course_design_sources(pack)
    normalized = course_source_catalog.normalize_course_sources(
        {"sources": projected}
    )

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
    )
    assert normalized[1].ref == "d71da420f1aa2ea39b61356e4f9900c6371e7a42"
    assert normalized[2].ref == "36a909f00c9478983a8d1b950440e2abc28b8a55"
    assert normalized[3].ref == "086995ece4260a3408740b94cfe2701ce24f8b57"
    assert all(source.files == ("README.md",) for source in normalized[1:])


def test_course_design_uses_exact_content_pack_source_projection() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)

    assert design["sources"] == project_course_design_sources(pack)


def test_draft_course_design_allocates_33_weeks_without_freezing_open_choices() -> None:
    design = load(DESIGN_PATH)
    year = design["years"][0]

    assert year["id"] == "quinto-anno"
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
    assert "Frontend framework" in year["udas"][5]["title"]


def test_public_and_licensed_references_are_separated_from_indexable_sources() -> None:
    pack = load(PACK_PATH)
    references = {item["id"]: item for item in pack["references"]}

    assert references["tpsi5-ref-mdn"]["role"] == "technical-reference"
    assert references["tpsi5-ref-whatwg-html"]["role"] == "specification"
    assert references["tpsi5-ref-rfc9110"]["role"] == "specification"
    assert references["tpsi5-ref-bootstrap"]["role"] == "technical-reference"
    assert references["tpsi5-ref-manning-css-depth"]["role"] == "teacher-reference"
    assert references["tpsi5-ref-manning-css-depth"]["access"] == "licensed"
    assert references["tpsi5-ref-pluralsight-javascript"]["role"] == "teacher-reference"
    assert references["tpsi5-ref-pluralsight-javascript"]["access"] == "licensed"

    source_providers = {source["provider"] for source in pack["sources"]}
    assert "mdn" not in source_providers
    assert "bootstrap" not in source_providers
    assert "manning" not in source_providers
    assert "pluralsight" not in source_providers


def test_framework_orm_and_typescript_remain_explicit_open_decisions() -> None:
    pack = load(PACK_PATH)
    decisions = pack["extensions"]["bootstrap_decisions"]

    assert decisions["frontend_framework"] == "tbd"
    assert decisions["node_orm"] == "tbd"
    assert decisions["typescript_depth"] == "tbd"
    assert decisions["main_backend"] == "node-express"
    assert decisions["python_mirror"] == "fastapi"


def test_legacy_code_repository_is_not_misrepresented_as_markdown_code_ingestion() -> None:
    pack = load(PACK_PATH)
    feisbuc = next(
        source
        for source in pack["sources"]
        if source["id"] == "tpsi5-source-feisbuc-legacy"
    )

    assert feisbuc["files"] == ["README.md"]
    assert feisbuc["provider"] == "github"
    assert feisbuc["ref"] == "086995ece4260a3408740b94cfe2701ce24f8b57"


def test_content_items_link_a_to_e_activities_and_provenance() -> None:
    pack = load(PACK_PATH)
    items = {item["id"]: item for item in pack["content_items"]}

    html_item = items["tpsi5-content-web-platform-html"]
    assert html_item["path"] == "content/tpsi5/01_WEB_PLATFORM_HTML_MODERNO.md"
    assert html_item["activity_ids"] == [
        "tpsi5-activity-a-html-anatomy-001",
        "tpsi5-activity-b-feisbuc-semantic-001",
    ]
    assert HTML_LESSON_PATH.is_file()

    css_item = items["tpsi5-content-css-modern-responsive"]
    assert css_item["path"] == "content/tpsi5/02_CSS_MODERNO_RESPONSIVE.md"
    assert css_item["activity_ids"] == [
        "tpsi5-activity-c-feisbuc-responsive-layout-001",
        "tpsi5-activity-d-debug-responsive-css-001",
        "tpsi5-activity-e-feisbuc-bootstrap-ui-001",
    ]
    assert CSS_LESSON_PATH.is_file()

    bootstrap_item = items["tpsi5-content-bootstrap-framework"]
    assert bootstrap_item["path"] == "content/tpsi5/03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md"
    assert bootstrap_item["activity_ids"] == [
        "tpsi5-activity-e-feisbuc-bootstrap-ui-001"
    ]
    source_ref_ids = {source_ref["id"] for source_ref in bootstrap_item["source_refs"]}
    assert {
        "tpsi5-source-originali",
        "tpsi5-ref-bootstrap",
        "tpsi5-ref-mdn",
        "tpsi5-ref-manning-css-depth",
    } <= source_ref_ids
    assert BOOTSTRAP_LESSON_PATH.is_file()


def test_uda21_schedules_html_css_and_bootstrap_lessons_with_activities() -> None:
    design = load(DESIGN_PATH)
    uda21 = next(uda for uda in design["years"][0]["udas"] if uda["id"] == "uda-21")

    assert len(uda21["items"]) == 3
    html_lesson, css_lesson, bootstrap_lesson = uda21["items"]

    assert html_lesson["source"] == "content/tpsi5/01_WEB_PLATFORM_HTML_MODERNO.md"
    assert html_lesson["activity_ids"] == [
        "tpsi5-activity-a-html-anatomy-001",
        "tpsi5-activity-b-feisbuc-semantic-001",
    ]

    assert css_lesson["source"] == "content/tpsi5/02_CSS_MODERNO_RESPONSIVE.md"
    assert css_lesson["activity_ids"] == [
        "tpsi5-activity-c-feisbuc-responsive-layout-001",
        "tpsi5-activity-d-debug-responsive-css-001",
    ]

    assert bootstrap_lesson["source"] == "content/tpsi5/03_BOOTSTRAP_DA_CSS_A_FRAMEWORK.md"
    assert bootstrap_lesson["activity_ids"] == [
        "tpsi5-activity-e-feisbuc-bootstrap-ui-001"
    ]
    assert all(item["frame"]["status"] == "draft" for item in uda21["items"])


def _assert_activity_contract(
    root: Path,
    difficulty: str,
    activity_id: str,
    expected_student_targets: set[str],
    known_content_ids: set[str],
) -> dict:
    path = root / "activity.json"
    activity = load(path)
    assert validate_activity(activity, str(path)) == []
    assert activity["id"] == activity_id
    assert activity["difficolta"] == difficulty
    assert activity["linguaggio"] == "html"
    assert set(activity["content_ids"]) <= known_content_ids
    assert activity["correzione"] == {
        "compila": False,
        "test": False,
        "sandbox": False,
        "ai_feedback": False,
    }
    assert sum(item["punti"] for item in activity["rubrica"]) == 10

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

    assert student_targets == expected_student_targets
    return activity


def test_level_a_to_e_activity_contracts_and_assets_are_valid() -> None:
    pack = load(PACK_PATH)
    known_content_ids = {item["id"] for item in pack["content_items"]}

    _assert_activity_contract(
        ACTIVITY_A_ROOT,
        "A",
        "tpsi5-activity-a-html-anatomy-001",
        {"index.html", "README.md"},
        known_content_ids,
    )
    _assert_activity_contract(
        ACTIVITY_B_ROOT,
        "B",
        "tpsi5-activity-b-feisbuc-semantic-001",
        {"index.html", "README.md"},
        known_content_ids,
    )
    activity_c = _assert_activity_contract(
        ACTIVITY_C_ROOT,
        "C",
        "tpsi5-activity-c-feisbuc-responsive-layout-001",
        {"index.html", "style.css", "README.md"},
        known_content_ids,
    )
    activity_d = _assert_activity_contract(
        ACTIVITY_D_ROOT,
        "D",
        "tpsi5-activity-d-debug-responsive-css-001",
        {"index.html", "style.css", "DIAGNOSI.md", "README.md"},
        known_content_ids,
    )
    activity_e = _assert_activity_contract(
        ACTIVITY_E_ROOT,
        "E",
        "tpsi5-activity-e-feisbuc-bootstrap-ui-001",
        {"index.html", "custom.css", "MAPPING.md", "README.md"},
        known_content_ids,
    )

    assert activity_c["project_milestone"] == "feisbuc-01-responsive-shell"
    assert activity_d["tipo"] == "debug-didattico"
    assert activity_e["project_milestone"] == "feisbuc-02-bootstrap-ui"


def test_html_auto_grading_is_not_claimed_before_platform_support_exists() -> None:
    assert SUPPORTED_LANGUAGES["html"] == "planned"
    for root in (
        ACTIVITY_A_ROOT,
        ACTIVITY_B_ROOT,
        ACTIVITY_C_ROOT,
        ACTIVITY_D_ROOT,
        ACTIVITY_E_ROOT,
    ):
        assert load(root / "activity.json")["correzione"]["test"] is False


def test_level_a_reference_solution_has_modern_document_metadata() -> None:
    solution = parse_html(ACTIVITY_A_ROOT / "solution" / "index.html")

    assert "doctype html" in solution.declarations
    assert solution.attrs["html"][0].get("lang") == "it"
    meta_attrs = solution.attrs["meta"]
    assert any(item.get("charset") == "utf-8" for item in meta_attrs)
    assert any(
        item.get("name") == "viewport"
        and item.get("content") == "width=device-width, initial-scale=1"
        for item in meta_attrs
    )
    assert solution.tags.count("header") == 1
    assert solution.tags.count("main") == 1
    assert solution.tags.count("h1") == 1


def test_feisbuc_milestone_zero_reference_solution_is_semantic() -> None:
    starter = parse_html(ACTIVITY_B_ROOT / "starter" / "index.html")
    solution = parse_html(ACTIVITY_B_ROOT / "solution" / "index.html")

    assert "header" not in starter.tags
    assert starter.tags.count("div") >= 6
    assert solution.tags.count("header") == 1
    assert solution.tags.count("nav") == 1
    assert solution.tags.count("main") == 1
    assert solution.tags.count("section") == 2
    assert solution.tags.count("article") == 2
    assert solution.tags.count("footer") == 1


def test_feisbuc_milestone_one_reference_css_uses_modern_layout_primitives() -> None:
    css = (ACTIVITY_C_ROOT / "solution" / "style.css").read_text(encoding="utf-8")

    for fragment in (
        "box-sizing: border-box",
        "display: grid",
        "grid-template-columns: 1fr",
        "@media (min-width: 56rem)",
        "minmax(0, 1fr)",
        "display: flex",
        "flex-wrap: wrap",
        "max-width: 100%",
        "gap:",
    ):
        assert fragment in css

    assert "float:" not in css
    assert "!important" not in css
    assert "overflow-x: hidden" not in css


def test_css_debug_starter_contains_declared_faults_and_solution_removes_them() -> None:
    starter = (ACTIVITY_D_ROOT / "starter" / "style.css").read_text(encoding="utf-8")
    solution = (ACTIVITY_D_ROOT / "solution" / "style.css").read_text(encoding="utf-8")
    diagnosis = (ACTIVITY_D_ROOT / "solution" / "DIAGNOSI.md").read_text(encoding="utf-8")

    assert "box-sizing: content-box" in starter
    assert "width: 1200px" in starter
    assert "grid-template-columns: 280px 700px 280px" in starter
    assert "min-width: 700px" in starter
    assert "!important" in starter
    assert "flex-wrap: nowrap" in starter

    assert "box-sizing: border-box" in solution
    assert "grid-template-columns: 1fr" in solution
    assert "minmax(0, 1fr)" in solution
    assert "flex-wrap: wrap" in solution
    assert "!important" not in solution
    assert "width: 1200px" not in solution
    assert "overflow-x: hidden" not in solution

    for keyword in ("body", "content-box", "min-width", "important", "media query"):
        assert keyword.lower() in diagnosis.lower()


def test_feisbuc_milestone_two_uses_bootstrap_as_abstraction_not_duplicate_layout() -> None:
    starter_css = (ACTIVITY_E_ROOT / "starter" / "custom.css").read_text(encoding="utf-8")
    solution_html = (ACTIVITY_E_ROOT / "solution" / "index.html").read_text(encoding="utf-8")
    solution_css = (ACTIVITY_E_ROOT / "solution" / "custom.css").read_text(encoding="utf-8")
    mapping = (ACTIVITY_E_ROOT / "solution" / "MAPPING.md").read_text(encoding="utf-8")
    parsed = parse_html(ACTIVITY_E_ROOT / "solution" / "index.html")
    bootstrap_classes = classes(parsed)

    assert "display: grid" in starter_css
    assert "display: flex" in starter_css
    assert "@media" in starter_css

    assert "bootstrap@5.3.8/dist/css/bootstrap.min.css" in solution_html
    assert "bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" in solution_html
    assert "sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" in solution_html
    assert "sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" in solution_html

    for expected_class in (
        "container",
        "row",
        "col-12",
        "col-lg-3",
        "col-lg-6",
        "navbar",
        "navbar-expand-lg",
        "card",
        "btn",
        "d-flex",
        "gap-2",
    ):
        assert expected_class in bootstrap_classes

    assert parsed.tags.count("article") == 2
    assert parsed.tags.count("h1") == 1
    assert any(
        attrs.get("data-bs-toggle") == "collapse"
        and attrs.get("data-bs-target") == "#mainNav"
        for attrs in parsed.attrs.get("button", [])
    )

    assert "display: grid" not in solution_css
    assert "display: flex" not in solution_css
    assert "@media" not in solution_css
    assert "!important" not in solution_css
    assert "style=" not in solution_html

    assert mapping.count("| ") >= 25
    assert "CSS nativo" in mapping
    assert "Bootstrap" in mapping
    assert "Flexbox" in mapping


def test_legacy_audit_records_html_and_css_migration_decisions() -> None:
    audit = (ROOT / "doc" / "LEGACY_REUSE_AUDIT.md").read_text(encoding="utf-8")

    assert "Decisioni per frammento — primo modulo HTML" in audit
    assert "`Scheletro html` | **rewrite**" in audit
    assert "`Tag ul` | **rewrite**" in audit
    assert "`CSS sintassi` | **migrated/rewrite**" in audit
    assert "`Box Model` | **migrated/major update**" in audit
    assert "feisbuc-00-semantic-skeleton" in audit
    assert "feisbuc-01-responsive-shell" in audit
