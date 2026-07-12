from __future__ import annotations

import re

from slopcheck.rules import Finding

COMMENT = re.compile(r"^\s*(#|//)\s*(.*)$")
DIVIDER = re.compile(r"^\s*(#|//)\s*[-=~*─═]{8,}\s*$")
SWALLOWED_ERROR = re.compile(
    r"except[^:]*:\s*pass\b|catch\s*\([^)]*\)\s*\{\s*\}"
)

# Comments that narrate what the next line already says.
NARRATION = re.compile(
    r"^(loop through|iterate over|check if|initialize|create a|create the|"
    r"define |return the|increment|call the|set the|import |get the|"
    r"this function|this method|this class|here we|here's|first,? we|"
    r"now we|finally,? we|make sure)",
    re.IGNORECASE,
)

CAP_NARRATION = 8
CAP_SWALLOWED = 6
CAP_DIVIDERS = 4


def check_code(path: str, text: str) -> list[Finding]:
    lines = text.splitlines()
    findings: list[Finding] = []
    findings += _narration_comments(path, lines)
    findings += _comment_ratio(path, lines)
    findings += _swallowed_errors(path, text)
    findings += _divider_comments(path, lines)
    return findings


def _narration_comments(path: str, lines: list[str]) -> list[Finding]:
    hits = []
    for i, line in enumerate(lines, 1):
        match = COMMENT.match(line)
        if match and NARRATION.match(match.group(2)):
            hits.append(i)
    if not hits:
        return []
    points = min(len(hits), CAP_NARRATION)
    return [
        Finding(
            path, hits[0], "narration-comment",
            f"{len(hits)} comment(s) narrating the code they sit on", points,
        )
    ]


def _comment_ratio(path: str, lines: list[str]) -> list[Finding]:
    code = sum(1 for line in lines if line.strip())
    comments = sum(1 for line in lines if COMMENT.match(line))
    if code < 30 or comments / code <= 0.4:
        return []
    return [
        Finding(
            path, 1, "comment-ratio",
            f"{comments} comment lines for {code} non-blank lines "
            f"({comments / code:.0%})",
            5,
        )
    ]


def _swallowed_errors(path: str, text: str) -> list[Finding]:
    hits = []
    for match in SWALLOWED_ERROR.finditer(text):
        hits.append(text.count("\n", 0, match.start()) + 1)
    if not hits:
        return []
    points = min(len(hits) * 2, CAP_SWALLOWED)
    return [
        Finding(
            path, hits[0], "swallowed-error",
            f"{len(hits)} silently swallowed exception(s)", points,
        )
    ]


def _divider_comments(path: str, lines: list[str]) -> list[Finding]:
    hits = [i for i, line in enumerate(lines, 1) if DIVIDER.match(line)]
    if len(hits) < 3:
        return []
    points = min(len(hits), CAP_DIVIDERS)
    return [
        Finding(
            path, hits[0], "divider-comment",
            f"{len(hits)} ASCII-art section dividers", points,
        )
    ]
