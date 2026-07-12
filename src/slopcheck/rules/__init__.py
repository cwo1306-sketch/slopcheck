from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

MARKDOWN_SUFFIXES = {".md", ".mdx", ".markdown"}
CODE_SUFFIXES = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rb",
    ".java", ".c", ".h", ".cpp", ".rs", ".sh", ".swift", ".kt",
}


@dataclass
class Finding:
    file: str
    line: int
    rule: str
    message: str
    points: int


def check_file(path: Path, text: str) -> list[Finding]:
    from slopcheck.rules.code import check_code
    from slopcheck.rules.markdown import check_markdown

    suffix = path.suffix.lower()
    if suffix in MARKDOWN_SUFFIXES:
        return check_markdown(str(path), text)
    if suffix in CODE_SUFFIXES:
        return check_code(str(path), text)
    return []
