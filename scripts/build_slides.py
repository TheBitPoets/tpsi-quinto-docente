#!/usr/bin/env python3
"""Validate and build TPSI5 Marp decks into HTML, PDF and PPTX artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SLIDES_ROOT = ROOT / "slides" / "tpsi5"
MODULES_ROOT = SLIDES_ROOT / "modules"
CONTENT_ROOT = ROOT / "content" / "tpsi5"
ROOT_README = ROOT / "README.md"
SLIDES_README = SLIDES_ROOT / "README.md"
MARP_CLI_VERSION = "4.5.0"
MARP_PACKAGE = f"@marp-team/marp-cli@{MARP_CLI_VERSION}"
MODULE_RE = re.compile(r"^(\d{2})_[A-Z0-9_]+\.md$")
EXPECTED_MODULES = tuple(f"{i:02d}" for i in range(19))


def discover_module_decks() -> list[Path]:
    return sorted(p for p in MODULES_ROOT.glob("*.md") if MODULE_RE.match(p.name))


def discover_decks() -> list[Path]:
    return [SLIDES_ROOT / "COURSE_SLIDES.md", *discover_module_decks()]


def _front_matter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    return "" if end < 0 else text[4:end]


def validate_sources() -> None:
    errors: list[str] = []
    modules = discover_module_decks()
    numbers = tuple(p.name[:2] for p in modules)
    if numbers != EXPECTED_MODULES:
        errors.append(f"expected module decks 00..18, found: {numbers}")

    content_files = sorted(
        p for p in CONTENT_ROOT.glob("[0-9][0-9]_*.md") if p.name[:2] in EXPECTED_MODULES
    )
    content_by_number = {p.name[:2]: p for p in content_files}
    for deck in modules:
        number = deck.name[:2]
        canonical = content_by_number.get(number)
        if canonical is None:
            errors.append(f"{deck}: no canonical content module {number}")
        elif deck.stem != canonical.stem:
            errors.append(
                f"{deck}: stem differs from canonical content {canonical.name}"
            )

        text = deck.read_text(encoding="utf-8")
        front_matter = _front_matter(text)
        if not front_matter:
            errors.append(f"{deck}: missing YAML front matter")
        elif not re.search(r"(?m)^marp:\s*true\s*$", front_matter):
            errors.append(f"{deck}: front matter must contain 'marp: true'")
        if "## Obiettivi" not in text and "# Obiettivi" not in text:
            errors.append(f"{deck}: missing objectives slide/section")
        if "checkpoint" not in text.lower():
            errors.append(f"{deck}: missing checkpoint")
        if "Feisbuc" not in text:
            errors.append(f"{deck}: missing Feisbuc connection")

    overview = SLIDES_ROOT / "COURSE_SLIDES.md"
    if not overview.exists():
        errors.append("missing slides/tpsi5/COURSE_SLIDES.md")
    else:
        fm = _front_matter(overview.read_text(encoding="utf-8"))
        if not fm or not re.search(r"(?m)^marp:\s*true\s*$", fm):
            errors.append("COURSE_SLIDES.md must be a Marp deck")

    for index_path in (ROOT_README, SLIDES_README):
        if not index_path.exists():
            errors.append(f"missing {index_path.relative_to(ROOT)}")
            continue
        index_text = index_path.read_text(encoding="utf-8")
        for deck in modules:
            expected = f"modules/{deck.name}"
            if index_path == ROOT_README:
                expected = f"slides/tpsi5/{expected}"
            if expected not in index_text:
                errors.append(
                    f"{index_path.relative_to(ROOT)}: missing link to {expected}"
                )

    if errors:
        raise SystemExit("Slide delivery validation failed:\n- " + "\n- ".join(errors))


def _run_marp(inputs: Iterable[Path], output_dir: Path, fmt: str, browser: str) -> None:
    npx = shutil.which("npx")
    if not npx:
        raise SystemExit("npx not found: install Node.js 18+ before building slides")

    output_dir.mkdir(parents=True, exist_ok=True)
    relative_inputs = [str(p.relative_to(ROOT)) for p in inputs]
    cmd = [
        npx,
        "--yes",
        MARP_PACKAGE,
        "--html",
        "--allow-local-files",
        "--input-dir",
        str(SLIDES_ROOT.relative_to(ROOT)),
        "--output",
        str(output_dir.relative_to(ROOT)),
        "--parallel",
        "4",
    ]
    if fmt == "pdf":
        cmd.extend(["--pdf", "--pdf-outlines", "--browser", browser])
    elif fmt == "pptx":
        cmd.extend(["--pptx", "--browser", browser])
    elif fmt != "html":
        raise ValueError(f"unsupported format: {fmt}")
    cmd.extend(relative_inputs)
    subprocess.run(cmd, cwd=ROOT, check=True)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(output_root: Path, formats: list[str]) -> None:
    files = []
    for path in sorted(output_root.rglob("*")):
        if not path.is_file() or path.name in {"MANIFEST.json", "SHA256SUMS.txt"}:
            continue
        files.append(
            {
                "path": path.relative_to(output_root).as_posix(),
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
            }
        )

    source_files = []
    for path in discover_decks():
        source_files.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": _sha256(path),
            }
        )

    manifest = {
        "schema": "thebitpoets.course-slides-artifact.v1",
        "course": "tpsi-quinto-2026-2027",
        "content_pack": "1.0.0",
        "marp_cli": MARP_CLI_VERSION,
        "commit": os.environ.get("GITHUB_SHA"),
        "formats": formats,
        "source_decks": source_files,
        "artifacts": files,
    }
    (output_root / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (output_root / "SHA256SUMS.txt").write_text(
        "".join(f"{item['sha256']}  {item['path']}\n" for item in files),
        encoding="utf-8",
    )


def build(output_root: Path, formats: list[str], browser: str) -> None:
    validate_sources()
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)
    decks = discover_decks()
    for fmt in formats:
        _run_marp(decks, output_root / fmt, fmt, browser)
    write_manifest(output_root, formats)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "build" / "tpsi5-slides",
        help="artifact output directory",
    )
    parser.add_argument(
        "--formats",
        default="html,pdf,pptx",
        help="comma-separated subset of html,pdf,pptx",
    )
    parser.add_argument("--browser", default="chrome")
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    formats = [part.strip() for part in args.formats.split(",") if part.strip()]
    invalid = sorted(set(formats) - {"html", "pdf", "pptx"})
    if invalid:
        raise SystemExit(f"unsupported formats: {', '.join(invalid)}")
    validate_sources()
    if args.check_only:
        print(f"OK: 19 modular decks + overview; Marp CLI pinned at {MARP_CLI_VERSION}")
        return 0
    output = args.output if args.output.is_absolute() else ROOT / args.output
    build(output, formats, args.browser)
    print(f"Built {len(discover_decks())} decks in {', '.join(formats)} -> {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
