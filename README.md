# slopcheck

**AI writes half your code now. Nobody reads it. slopcheck does.**

A linter that detects AI slop in your repo — built with zero AI and zero
dependencies, because it takes a human to catch a machine.

You know the signs: emoji-studded READMEs, comments that narrate the line below
them, `except: pass` scattered like confetti, and the word "delve". slopcheck
reads your repo the way a tired reviewer does — and hands it a score.

```
$ slopcheck .

README.md
  ⚠ 4 heading(s) decorated with emoji [emoji-heading, L1] (+6)
  ⚠ "seamless" [buzzword, L3] (+1)
  ⚠ "delve" [buzzword, L7] (+1)

src/utils.py
  ⚠ 6 comment(s) narrating the code they sit on [narration-comment, L2] (+6)
  ⚠ 2 silently swallowed exception(s) [swallowed-error, L41] (+4)

Slop Score: 23/100 — Mostly Human™ (5 finding(s), 12 file(s))
```

No network calls, no model, no telemetry. Every check is a regex a human can read.
Run on itself, this repo scores 2/100 — the rule table below quotes the evidence,
and slopcheck does not accept excuses. Certified Human, barely.

## Install

```sh
pip install slopcheck        # or: uv tool install slopcheck
```

Or run it straight from a checkout, since there are no dependencies:

```sh
python -m slopcheck .
```

## Usage

```sh
slopcheck                    # scan the current directory
slopcheck src/ README.md     # scan specific paths
slopcheck --commits          # also grade recent git commit subjects
slopcheck --json             # machine-readable output
slopcheck --fail-over 40     # exit 1 if the score exceeds 40 (for CI)
```

## What it looks for

| Rule | Signal |
| --- | --- |
| `emoji-heading` | Markdown headings decorated with emoji |
| `buzzword` | "delve", "seamless", "robust", "unlock the full potential", ... |
| `emoji-density` | More than 2 emoji per 100 words of prose |
| `ai-confession` | The document admits it was generated |
| `narration-comment` | Comments that restate the line below them |
| `comment-ratio` | More than 40% of non-blank lines are comments |
| `swallowed-error` | `except: pass` and empty `catch` blocks |
| `divider-comment` | Three or more ASCII-art section dividers |
| `emoji-commit` | Commit subjects that lead with emoji (`--commits`) |
| `commit-narration` | Subjects opening with "This commit..." (`--commits`) |

Each rule is capped, and a file's score saturates, so one enthusiastic README
cannot condemn an otherwise clean codebase. The repo score is the average over
scanned files.

## Scoring

| Score | Verdict |
| --- | --- |
| 0–9 | Certified Human |
| 10–29 | Mostly Human™ |
| 30–59 | Slop Suspected |
| 60–84 | Heavy Slop |
| 85–100 | Pure Slop |

A high score doesn't prove a machine wrote it — plenty of humans wrote like this
before 2022. It proves nobody read it after it was written. That's what slop is.

## Development

```sh
uv run --group dev pytest
```

Adding a rule: drop a function in `src/slopcheck/rules/markdown.py` or
`code.py`, return `Finding`s, cap the points, and add a test. Rules must be
explainable in one sentence; if it needs a model, it doesn't belong here.

## License

MIT
