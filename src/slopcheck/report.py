from __future__ import annotations

import json
import sys
from itertools import groupby

from slopcheck.rules import Finding

# A file saturates at 100; the repo score is the mean over scanned files,
# so one sloppy README can't condemn a large clean codebase.
FILE_SCALE = 5

LABELS = [
    (10, "Certified Human"),
    (30, "Mostly Human™"),
    (60, "Slop Suspected"),
    (85, "Heavy Slop"),
    (101, "Pure Slop"),
]


def score(findings: list[Finding], files_scanned: int) -> int:
    if files_scanned == 0:
        return 0
    per_file: dict[str, int] = {}
    for finding in findings:
        per_file[finding.file] = per_file.get(finding.file, 0) + finding.points
    total = sum(min(points * FILE_SCALE, 100) for points in per_file.values())
    return min(100, round(total / files_scanned))


def label(value: int) -> str:
    for threshold, name in LABELS:
        if value < threshold:
            return name
    return LABELS[-1][1]


def render(findings: list[Finding], files_scanned: int, color: bool) -> str:
    dim, warn, bold, reset = (
        ("\033[2m", "\033[33m", "\033[1m", "\033[0m") if color
        else ("", "", "", "")
    )
    out: list[str] = []
    for file, group in groupby(findings, key=lambda f: f.file):
        out.append(f"\n{bold}{file}{reset}")
        for f in group:
            location = f"L{f.line}" if f.line else "-"
            out.append(
                f"  {warn}⚠{reset} {f.message} "
                f"{dim}[{f.rule}, {location}] (+{f.points}){reset}"
            )
    value = score(findings, files_scanned)
    out.append(
        f"\n{bold}Slop Score: {value}/100 — {label(value)}{reset}"
        f" {dim}({len(findings)} finding(s), {files_scanned} file(s)){reset}"
    )
    return "\n".join(out)


def render_json(findings: list[Finding], files_scanned: int) -> str:
    value = score(findings, files_scanned)
    return json.dumps(
        {
            "score": value,
            "label": label(value),
            "files_scanned": files_scanned,
            "findings": [vars(f) for f in findings],
        },
        indent=2,
        ensure_ascii=False,
    )


def use_color(no_color_flag: bool) -> bool:
    return not no_color_flag and sys.stdout.isatty()
