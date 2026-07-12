from __future__ import annotations

import re
import subprocess

from slopcheck.rules import Finding
from slopcheck.rules.markdown import EMOJI

CONVENTIONAL_EMOJI = re.compile(r"^(\w+(\([^)]*\))?:)?\s*" + EMOJI.pattern)
VERBOSE_OPENER = re.compile(
    r"^(this commit|this change|in this commit)", re.IGNORECASE
)

CAP_EMOJI_SUBJECTS = 6


def check_commits(repo: str, limit: int = 50) -> list[Finding]:
    try:
        out = subprocess.run(
            ["git", "-C", repo, "log", f"-{limit}", "--format=%s"],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if out.returncode != 0:
        return []

    subjects = [s for s in out.stdout.splitlines() if s.strip()]
    findings: list[Finding] = []

    emoji_subjects = [s for s in subjects if CONVENTIONAL_EMOJI.match(s)]
    if emoji_subjects:
        points = min(len(emoji_subjects), CAP_EMOJI_SUBJECTS)
        findings.append(
            Finding(
                "git log", 0, "emoji-commit",
                f"{len(emoji_subjects)} of last {len(subjects)} commit "
                f"subjects lead with emoji",
                points,
            )
        )

    verbose = [s for s in subjects if VERBOSE_OPENER.match(s)]
    if verbose:
        findings.append(
            Finding(
                "git log", 0, "commit-narration",
                f'{len(verbose)} subject(s) open with "This commit..."',
                min(len(verbose) * 2, 6),
            )
        )
    return findings
