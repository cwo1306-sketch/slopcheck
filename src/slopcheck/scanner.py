from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from slopcheck.rules import CODE_SUFFIXES, MARKDOWN_SUFFIXES

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__",
    "dist", "build", ".mypy_cache", ".ruff_cache", ".tox", "vendor",
}
MAX_BYTES = 1_000_000
SUFFIXES = CODE_SUFFIXES | MARKDOWN_SUFFIXES


def collect_files(paths: list[str]) -> Iterator[Path]:
    for raw in paths:
        root = Path(raw)
        if root.is_file():
            if root.suffix.lower() in SUFFIXES:
                yield root
            continue
        for path in sorted(root.rglob("*")):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if not path.is_file() or path.suffix.lower() not in SUFFIXES:
                continue
            try:
                if path.stat().st_size > MAX_BYTES:
                    continue
            except OSError:
                continue
            yield path


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
