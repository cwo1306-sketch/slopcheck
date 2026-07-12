from slopcheck.rules.markdown import check_markdown


def rules_of(findings):
    return {f.rule for f in findings}


def test_clean_markdown_has_no_findings():
    text = "# slopcheck\n\nA linter for AI slop.\n\n## Install\n\npip install slopcheck\n"
    assert check_markdown("README.md", text) == []


def test_emoji_headings_collapse_into_one_finding():
    text = "# 🚀 Start\n\n## ✨ Features\n\n## 🔥 Usage\n"
    findings = [f for f in check_markdown("x.md", text) if f.rule == "emoji-heading"]
    assert len(findings) == 1
    assert "3 heading(s)" in findings[0].message
    assert findings[0].points == 6


def test_buzzwords_reported_once_each():
    text = "We delve into robust solutions. Truly robust. We delve again.\n"
    findings = [f for f in check_markdown("x.md", text) if f.rule == "buzzword"]
    assert {f.message for f in findings} == {'"delve"', '"robust"'}


def test_buzzword_points_capped():
    text = " ".join(
        ["delve seamless leverage robust comprehensive cutting-edge",
         "state-of-the-art game-changer revolutionize empower elevate"]
    )
    findings = [f for f in check_markdown("x.md", text) if f.rule == "buzzword"]
    assert sum(f.points for f in findings) == 8


def test_emoji_density_needs_enough_words():
    text = "🚀 " * 10
    assert check_markdown("x.md", text) == []


def test_ai_confession():
    text = "word " * 60 + "\nThis README was generated with AI.\n"
    findings = check_markdown("x.md", text)
    assert "ai-confession" in rules_of(findings)
