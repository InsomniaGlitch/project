import subprocess
import sys


def test_flake8():
    result = subprocess.run(
        [sys.executable, "-m", "flake8", "src/", "tests/"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Flake8 ошибки:\n{result.stdout}"
