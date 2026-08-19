from __future__ import annotations

import json
from pathlib import Path

from scripts import course_source_catalog
from scripts.content_pack_contract import (
    project_course_design_sources,
    validate_content_pack,
)


ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content" / "tpsi5" / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quinto_2026_2027.json"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_native_content_pack_v1_is_valid() -> None:
    pack = load(PACK_PATH)

    assert pack["schema_version"] == "thebitlab.content-pack.v1"
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
