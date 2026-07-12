from slopcheck.rules.code import check_code


def test_clean_code_has_no_findings():
    text = "def add(a, b):\n    return a + b\n"
    assert check_code("x.py", text) == []


def test_narration_comments_grouped():
    text = (
        "# Initialize the counter\n"
        "count = 0\n"
        "# Loop through the items\n"
        "for item in items:\n"
        "    # Increment the counter\n"
        "    count += 1\n"
    )
    findings = check_code("x.py", text)
    assert len(findings) == 1
    assert findings[0].rule == "narration-comment"
    assert "3 comment(s)" in findings[0].message


def test_why_comments_are_not_narration():
    text = "# NFC tags cap payloads at 137 bytes on this reader\nCHUNK = 137\n"
    assert check_code("x.py", text) == []


def test_swallowed_errors_python_and_js():
    py = "try:\n    x()\nexcept Exception:\n    pass\n"
    js = "try { x() } catch (e) {}\n"
    assert check_code("x.py", py)[0].rule == "swallowed-error"
    assert check_code("x.js", js)[0].rule == "swallowed-error"


def test_comment_ratio_needs_enough_code():
    lines = ["# a comment", "x = 1"] * 20
    findings = check_code("x.py", "\n".join(lines))
    assert any(f.rule == "comment-ratio" for f in findings)

    short = ["# a comment", "x = 1"] * 10
    findings = check_code("x.py", "\n".join(short))
    assert not any(f.rule == "comment-ratio" for f in findings)


def test_dividers_need_three_hits():
    two = "# ========\nx = 1\n# ========\n"
    three = two + "# ========\n"
    assert not any(f.rule == "divider-comment" for f in check_code("x.py", two))
    assert any(f.rule == "divider-comment" for f in check_code("x.py", three))
