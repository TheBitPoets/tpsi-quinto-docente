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

    content_by_number = {
        p.name[:2]: p
        for p in CONTENT_ROOT.glob("[0-9][0-9]_*.md")
        if p.name[:2] in EXPECTED_MODULES
    }
    slide_index = SLIDES_README.read_text(encoding="utf-8") if SLIDES_README.exists() else ""

    for deck in modules:
        number = deck.name[:2]
        canonical = content_by_number.get(number)
        if canonical is None:
            errors.append(f"{deck}: no canonical content module {number}")
        elif deck.stem != canonical.stem:
            errors.append(f"{deck}: stem differs from canonical content {canonical.name}")

        text = deck.read_text(encoding="utf-8")
        fm = _front_matter(text)
        if not fm or not re.search(r"(?m)^marp:\s*true\s*$", fm):
            errors.append(f"{deck}: missing Marp front matter")
        if "obiettivi" not in text.lower():
            errors.append(f"{deck}: missing objectives")
        if "checkpoint" not in text.lower():
            errors.append(f"{deck}: missing checkpoint")
        if "feisbuc" not in text.lower():
            errors.append(f"{deck}: missing Feisbuc connection")
        if f"modules/{deck.name}" not in slide_index:
            errors.append(f"slides/tpsi5/README.md: missing link to modules/{deck.name}")

    overview = SLIDES_ROOT / "COURSE_SLIDES.md"
    if not overview.exists():
        errors.append("missing slides/tpsi5/COURSE_SLIDES.md")
    else:
        fm = _front_matter(overview.read_text(encoding="utf-8"))
        if not fm or not re.search(r"(?m)^marp:\s*true\s*$", fm):
            errors.append("COURSE_SLIDES.md must be a Marp deck")

    root_index = ROOT_README.read_text(encoding="utf-8") if ROOT_README.exists() else ""
    for required in ("slides/tpsi5/README.md", "slides/tpsi5/COURSE_SLIDES.md"):
        if required not in root_index:
            errors.append(f"README.md: missing slide entry point {required}")

    if errors:
        raise SystemExit("Slide delivery validation failed:\n- " + "\n- ".join(errors))


def _generated_path(source: Path, fmt: str) -> Path:
    return source.with_suffix(f".{fmt}")


def _run_marp(inputs: Iterable[Path], output_dir: Path, fmt: str, browser: str) -> None:
    npx = shutil.which("npx")
    if not npx:
        raise SystemExit("npx not found: install Node.js 18+ before building slides")

    decks = list(inputs)
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = [_generated_path(source, fmt) for source in decks]
    for path in generated:
        path.unlink(missing_ok=True)

    parallelism = "1" if fmt == "pptx" else "4"
    cmd = [
        npx,
        "--yes",
        MARP_PACKAGE,
        "--html",
        "--allow-local-files",
        "--parallel",
        parallelism,
    ]
    if fmt == "pdf":
        cmd.extend(["--pdf", "--pdf-outlines", "--browser", browser])
    elif fmt == "pptx":
        cmd.extend(["--pptx", "--browser", browser])
    elif fmt != "html":
        raise ValueError(f"unsupported format: {fmt}")
    cmd.extend(str(p.relative_to(ROOT)) for p in decks)

    try:
        subprocess.run(cmd, cwd=ROOT, check=True)
        for source, built in zip(decks, generated):
            if not built.exists():
                raise SystemExit(f"Marp did not produce expected artifact: {built}")
            relative = source.relative_to(SLIDES_ROOT).with_suffix(f".{fmt}")
            destination = output_dir / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(built), str(destination))
    finally:
        for path in generated:
            path.unlink(missing_ok=True)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(output_root: Path, formats: list[str]) -> None:
    artifacts = []
    for path in sorted(output_root.rglob("*")):
        if path.is_file() and path.name not in {"MANIFEST.json", "SHA256SUMS.txt"}:
            artifacts.append({
                "path": path.relative_to(output_root).as_posix(),
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
            })
    sources = [
        {"path": p.relative_to(ROOT).as_posix(), "sha256": _sha256(p)}
        for p in discover_decks()
    ]
    manifest = {
        "schema": "thebitpoets.course-slides-artifact.v1",
        "course": "tpsi-quinto-2026-2027",
        "content_pack": "1.0.0",
        "marp_cli": MARP_CLI_VERSION,
        "commit": os.environ.get("SOURCE_SHA") or os.environ.get("GITHUB_SHA"),
        "formats": formats,
        "source_decks": sources,
        "artifacts": artifacts,
    }
    (output_root / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (output_root / "SHA256SUMS.txt").write_text(
        "".join(f"{item['sha256']}  {item['path']}\n" for item in artifacts), encoding="utf-8"
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
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "tpsi5-slides")
    parser.add_argument("--formats", default="html,pdf,pptx")
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
