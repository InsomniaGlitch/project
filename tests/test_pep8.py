import pycodestyle


def test_pep8():
    style = pycodestyle.StyleGuide(quiet=False)
    result = style.check_files(["src/", "tests/"])
    assert result.total_errors == 0, f"PEP8 нарушений: {result.total_errors}"
