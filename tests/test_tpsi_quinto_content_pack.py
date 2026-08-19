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
LESSON_PATH = ROOT / "content" / "tpsi5" / "01_WEB_PLATFORM_HTML_MODERNO.md"
ACTIVITY_A_ROOT = ROOT / "activities" / "tpsi5" / "html_anatomy_a"
ACTIVITY_B_ROOT = ROOT / "activities" / "tpsi5" / "feisbuc_semantic_b"


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


def test_native_content_pack_v1_is_valid() -> None:
    pack = load(PACK_PATH)

    assert pack["schema_version"] == "thebitlab.content-pack.v1"
    assert pack["version"] == "0.2.0"
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
    assert references["tpsi5-ref-manning-css-depth"]["role"] == "teacher-reference"
    assert references["tpsi5-ref-manning-css-depth"]["access"] == "licensed"
    assert references["tpsi5-ref-pluralsight-javascript"]["role"] == "teacher-reference"
    assert references["tpsi5-ref-pluralsight-javascript"]["access"] == "licensed"

    source_providers = {source["provider"] for source in pack["sources"]}
    assert "mdn" not in source_providers
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


def test_web_platform_html_content_item_links_level_a_and_b_activities() -> None:
    pack = load(PACK_PATH)
    item = next(
        content
        for content in pack["content_items"]
        if content["id"] == "tpsi5-content-web-platform-html"
    )

    assert item["path"] == "content/tpsi5/01_WEB_PLATFORM_HTML_MODERNO.md"
    assert item["activity_ids"] == [
        "tpsi5-activity-a-html-anatomy-001",
        "tpsi5-activity-b-feisbuc-semantic-001",
    ]
    source_ref_ids = {source_ref["id"] for source_ref in item["source_refs"]}
    assert {
        "tpsi5-source-originali",
        "tpsi5-source-html-css-legacy",
        "tpsi5-ref-mdn",
        "tpsi5-ref-whatwg-html",
    } <= source_ref_ids
    assert LESSON_PATH.is_file()


def test_uda21_schedules_html_lesson_and_activities() -> None:
    design = load(DESIGN_PATH)
    uda21 = next(uda for uda in design["years"][0]["udas"] if uda["id"] == "uda-21")

    assert len(uda21["items"]) == 1
    lesson = uda21["items"][0]
    assert lesson["source"] == "content/tpsi5/01_WEB_PLATFORM_HTML_MODERNO.md"
    assert lesson["activity_ids"] == [
        "tpsi5-activity-a-html-anatomy-001",
        "tpsi5-activity-b-feisbuc-semantic-001",
    ]
    assert lesson["frame"]["status"] == "draft"


def test_level_a_and_b_activity_contracts_and_assets_are_valid() -> None:
    pack = load(PACK_PATH)
    known_content_ids = {item["id"] for item in pack["content_items"]}
    expected = [
        (ACTIVITY_A_ROOT, "A", "tpsi5-activity-a-html-anatomy-001"),
        (ACTIVITY_B_ROOT, "B", "tpsi5-activity-b-feisbuc-semantic-001"),
    ]

    for root, difficulty, activity_id in expected:
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

        assert student_targets == {"index.html", "README.md"}


def test_html_auto_grading_is_not_claimed_before_platform_support_exists() -> None:
    assert SUPPORTED_LANGUAGES["html"] == "planned"
    assert load(ACTIVITY_A_ROOT / "activity.json")["correzione"]["test"] is False
    assert load(ACTIVITY_B_ROOT / "activity.json")["correzione"]["test"] is False


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


def test_feisbuc_milestone_reference_solution_is_semantic() -> None:
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
    assert solution.tags.count("h1") == 1
    assert solution.tags.count("h2") == 2
    assert solution.tags.count("h3") == 2
    assert solution.attrs["nav"][0].get("aria-label") == "Navigazione principale"
    feed = next(item for item in solution.attrs["section"] if item.get("id") == "feed")
    assert feed.get("aria-labelledby") == "feed-title"


def test_legacy_audit_records_first_html_migration_decisions() -> None:
    audit = (ROOT / "doc" / "LEGACY_REUSE_AUDIT.md").read_text(encoding="utf-8")

    assert "Decisioni per frammento — primo modulo HTML" in audit
    assert "`Scheletro html` | **rewrite**" in audit
    assert "`Tag ul` | **rewrite**" in audit
    assert "feisbuc-00-semantic-skeleton" in audit
