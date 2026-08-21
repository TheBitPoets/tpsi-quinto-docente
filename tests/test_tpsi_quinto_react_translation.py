from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_activity import validate_activity

ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "content" / "tpsi5" / "content-pack.json"
DESIGN_PATH = ROOT / "doc" / "course_designs" / "tpsi_quinto_2026_2027.json"
LESSON_PATH = ROOT / "content" / "tpsi5" / "14_REACT_TRANSLATION_COMPARISON.md"
A_ROOT = ROOT / "activities" / "tpsi5" / "react_translation_microscope_a"
B_ROOT = ROOT / "activities" / "tpsi5" / "react_post_card_b"

REACT_VERSION = "19.2.8"
PLUGIN_REACT_VERSION = "6.0.5"
VITE_VERSION = "8.2.1"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def assert_activity(root: Path, difficulty: str, activity_id: str) -> dict:
    activity = load(root / "activity.json")
    assert validate_activity(activity, str(root / "activity.json")) == []
    assert activity["id"] == activity_id
    assert activity["difficolta"] == difficulty
    assert activity["contesto"]["uda"] == "uda-25"
    assert activity["correzione"] == {
        "compila": False,
        "test": False,
        "sandbox": False,
        "ai_feedback": False,
    }
    assert sum(entry["punti"] for entry in activity["rubrica"]) == 10
    assert "project_milestone" not in activity
    for asset in activity["assets"]:
        assert (root / asset["path"]).is_file(), asset
        if asset["visibility"] == "student":
            assert asset.get("target_path")
    return activity


def assert_react_package(path: Path) -> None:
    package = load(path)
    assert package["dependencies"] == {
        "react": REACT_VERSION,
        "react-dom": REACT_VERSION,
    }
    assert package["devDependencies"] == {
        "@vitejs/plugin-react": PLUGIN_REACT_VERSION,
        "vite": VITE_VERSION,
    }
    assert package["engines"]["node"] == ">=22.18"


def test_react_translation_pack_design_and_activity_contracts() -> None:
    pack = load(PACK_PATH)
    design = load(DESIGN_PATH)

    assert pack["version"] == "0.19.0"
    assert pack["extensions"]["bootstrap_decisions"]["frontend_framework"] == "vue3-vite"

    refs = {entry["id"]: entry for entry in pack["references"]}
    react_ref = refs["tpsi5-ref-react"]
    assert react_ref["role"] == "technical-reference"
    assert "translation" in react_ref["title"].lower()
    assert REACT_VERSION in react_ref["notes"]
    assert PLUGIN_REACT_VERSION in react_ref["notes"]

    item = next(
        entry for entry in pack["content_items"]
        if entry["id"] == "tpsi5-content-react-translation-comparison"
    )
    assert item["order"] == 15
    assert item["path"] == "content/tpsi5/14_REACT_TRANSLATION_COMPARISON.md"
    assert item["activity_ids"] == [
        "tpsi5-activity-a-react-translation-microscope-001",
        "tpsi5-activity-b-react-post-card-translation-001",
    ]
    assert LESSON_PATH.is_file()

    uda25 = next(u for u in design["years"][0]["udas"] if u["id"] == "uda-25")
    assert uda25["weeks"] == "5"
    assert len(uda25["items"]) == 5
    assert uda25["items"][4]["source"] == item["path"]
    assert uda25["items"][4]["activity_ids"] == item["activity_ids"]
    assert "FastAPI" in uda25["items"][4]["frame"]["next_step"]
    assert "secondo frontend core" in uda25["items"][4]["frame"]["next_step"]

    assert_activity(A_ROOT, "A", "tpsi5-activity-a-react-translation-microscope-001")
    assert_activity(B_ROOT, "B", "tpsi5-activity-b-react-post-card-translation-001")


def test_react_translation_toolchain_is_pinned_and_reference_builds_exist() -> None:
    assert_react_package(A_ROOT / "starter" / "package.json")
    assert_react_package(B_ROOT / "starter" / "package.json")
    assert_react_package(B_ROOT / "solution" / "package.json")

    assert (A_ROOT / "starter" / "node_modules" / "react").is_dir()
    assert (A_ROOT / "starter" / "dist" / "index.html").is_file()
    assert (B_ROOT / "solution" / "node_modules" / "react").is_dir()
    assert (B_ROOT / "solution" / "dist" / "index.html").is_file()


def test_counter_translation_keeps_derived_state_simple() -> None:
    react_source = (A_ROOT / "starter" / "src" / "App.jsx").read_text(encoding="utf-8")
    vue_source = (A_ROOT / "starter" / "comparison" / "Counter.vue").read_text(encoding="utf-8")
    mapping = (A_ROOT / "solution" / "MAPPING.md").read_text(encoding="utf-8")

    assert "useState" in react_source
    assert "const doubled = count * 2" in react_source
    assert "useMemo" not in react_source
    assert "useState(0)" in react_source
    assert "ref(0)" in vue_source
    assert "computed(" in vue_source
    assert "useMemo" in mapping
    assert "ottimizzazione" in mapping.lower()


def test_postcard_translation_preserves_one_way_data_flow() -> None:
    child = (B_ROOT / "solution" / "src" / "components" / "PostCard.jsx").read_text(
        encoding="utf-8"
    )
    parent = (B_ROOT / "solution" / "src" / "App.jsx").read_text(encoding="utf-8")
    package_text = (B_ROOT / "solution" / "package.json").read_text(encoding="utf-8").lower()

    assert "onToggleLike(post.id)" in child
    assert "onDelete(post.id)" in child
    assert "canDelete ?" in child
    assert "fetch(" not in child
    assert "axios" not in child.lower()
    assert "post.liked =" not in child

    assert "setPosts((current) =>" in parent
    assert "current.map(" in parent
    assert "current.filter(" in parent
    assert "...post" in parent
    assert "key={post.id}" in parent

    combined = (child + parent + package_text).lower()
    for forbidden in ("react-router", "redux", "next.js", "\"next\""):
        assert forbidden not in combined
