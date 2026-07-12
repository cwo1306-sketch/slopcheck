from __future__ import annotations

import argparse

from slopcheck import __version__
from slopcheck.report import render, render_json, score, use_color
from slopcheck.rules import Finding, check_file
from slopcheck.rules.commits import check_commits
from slopcheck.scanner import collect_files, read_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="slopcheck",
        description="Detect AI slop in your repo. No AI was used, or harmed.",
    )
    parser.add_argument("paths", nargs="*", default=["."], help="files or directories to scan")
    parser.add_argument("--commits", action="store_true", help="also inspect recent git commit subjects")
    parser.add_argument("--fail-over", type=int, metavar="N", help="exit 1 if slop score exceeds N")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--no-color", action="store_true")
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(argv)

    findings: list[Finding] = []
    files_scanned = 0
    for path in collect_files(args.paths):
        text = read_text(path)
        if text is None:
            continue
        files_scanned += 1
        findings.extend(check_file(path, text))

    if args.commits:
        commit_findings = check_commits(args.paths[0])
        if commit_findings:
            files_scanned += 1
            findings.extend(commit_findings)

    if args.json:
        print(render_json(findings, files_scanned))
    else:
        print(render(findings, files_scanned, use_color(args.no_color)))

    if args.fail_over is not None:
        return 1 if score(findings, files_scanned) > args.fail_over else 0
    return 0
