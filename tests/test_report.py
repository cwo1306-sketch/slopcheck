from slopcheck.report import label, score
from slopcheck.rules import Finding


def finding(file, points):
    return Finding(file, 1, "buzzword", "x", points)


def test_score_empty():
    assert score([], 0) == 0
    assert score([], 10) == 0


def test_score_is_per_file_average():
    findings = [finding("a.md", 4)]
    assert score(findings, 1) == 20
    assert score(findings, 4) == 5


def test_file_score_saturates_at_100():
    findings = [finding("a.md", 999)]
    assert score(findings, 1) == 100


def test_labels():
    assert label(0) == "Certified Human"
    assert label(29) == "Mostly Human™"
    assert label(59) == "Slop Suspected"
    assert label(84) == "Heavy Slop"
    assert label(100) == "Pure Slop"
