#!/usr/bin/env python3
"""Build standalone TPSI5 SVG diagrams from reusable visual-system symbols."""

from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
VISUAL_ROOT = ROOT / "assets" / "tpsi5" / "visual-system"
COMPONENTS = VISUAL_ROOT / "components.svg"
SCENES = VISUAL_ROOT / "scenes"
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)


def qname(name: str) -> str:
    return f"{{{SVG_NS}}}{name}"


def load_component_defs() -> tuple[list[ET.Element], set[str]]:
    root = ET.parse(COMPONENTS).getroot()
    defs = root.find(qname("defs"))
    if defs is None:
        raise SystemExit(f"{COMPONENTS}: missing <defs>")
    items = [deepcopy(child) for child in list(defs)]
    ids = {
        node.attrib["id"]
        for child in items
        for node in child.iter()
        if "id" in node.attrib
    }
    ids.update(child.attrib["id"] for child in items if "id" in child.attrib)
    return items, ids


def render_scene(path: Path, component_defs: list[ET.Element], ids: set[str]) -> tuple[Path, bytes]:
    tree = ET.parse(path)
    root = tree.getroot()
    output_value = root.attrib.pop("data-output", None)
    if not output_value:
        raise SystemExit(f"{path}: missing data-output")
    output = (path.parent / output_value).resolve()
    allowed_root = (ROOT / "assets" / "tpsi5").resolve()
    if output != allowed_root and allowed_root not in output.parents:
        raise SystemExit(f"{path}: output escapes assets/tpsi5: {output}")

    placeholder = None
    for defs in root.findall(qname("defs")):
        if defs.attrib.get("id") == "visual-kit-components":
            placeholder = defs
            break
    if placeholder is None:
        raise SystemExit(f"{path}: missing <defs id='visual-kit-components'>")
    placeholder.attrib.pop("id", None)
    placeholder.extend(deepcopy(component_defs))

    for use in root.iter(qname("use")):
        href = use.attrib.get("href") or use.attrib.get(f"{{{XLINK_NS}}}href")
        if not href or not href.startswith("#tpsi-"):
            raise SystemExit(f"{path}: invalid component reference: {href!r}")
        if href[1:] not in ids:
            raise SystemExit(f"{path}: unknown component: {href}")

    ET.indent(tree, space="  ")
    payload = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    return output, payload


def build(check: bool) -> int:
    component_defs, ids = load_component_defs()
    scenes = sorted(SCENES.glob("*.scene.svg"))
    if not scenes:
        raise SystemExit(f"no scene sources found in {SCENES}")

    stale: list[Path] = []
    for scene in scenes:
        output, payload = render_scene(scene, component_defs, ids)
        if check:
            if not output.exists() or output.read_bytes() != payload:
                stale.append(output)
            continue
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(payload)
        print(f"built {output.relative_to(ROOT)}")

    if stale:
        print("Generated diagrams are stale:", file=sys.stderr)
        for path in stale:
            print(f"- {path.relative_to(ROOT)}", file=sys.stderr)
        print("Run: python3 scripts/build_course_diagrams.py", file=sys.stderr)
        return 1
    if check:
        print(f"OK: {len(scenes)} generated diagrams are up to date")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return build(args.check)


if __name__ == "__main__":
    raise SystemExit(main())
