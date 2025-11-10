import subprocess
from pathlib import Path

def test_cli_generates_svg(tmp_path):
    out = tmp_path / "t.svg"
    cmd = [
        "python", "-m", "src.cli",
        "--mode", "text",
        "--data", "hello",
        "--outfile", str(out)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert out.exists()