import json

from slopcheck.cli import main


def test_scans_directory_and_scores(tmp_path, capsys):
    (tmp_path / "README.md").write_text(
        "# 🚀 Project\n\nWe delve into robust, seamless solutions. " + "word " * 60
    )
    (tmp_path / "app.py").write_text(
        "# Initialize the counter\ncount = 0\n"
        "try:\n    run()\nexcept Exception:\n    pass\n"
    )
    assert main([str(tmp_path), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["files_scanned"] == 2
    assert data["score"] > 0
    rules = {f["rule"] for f in data["findings"]}
    assert {"emoji-heading", "buzzword", "narration-comment", "swallowed-error"} <= rules


def test_fail_over_threshold(tmp_path, capsys):
    (tmp_path / "README.md").write_text("# 🚀🔥✨ delve seamless robust\n" + "word " * 60)
    assert main([str(tmp_path), "--fail-over", "0", "--no-color"]) == 1
    assert main([str(tmp_path), "--fail-over", "100", "--no-color"]) == 0


def test_clean_repo_is_certified_human(tmp_path, capsys):
    (tmp_path / "README.md").write_text("# tool\n\nDoes one thing.\n")
    assert main([str(tmp_path), "--no-color"]) == 0
    assert "Certified Human" in capsys.readouterr().out
