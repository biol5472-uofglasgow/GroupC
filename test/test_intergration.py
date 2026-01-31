import subprocess
import sys
import shutil
from pathlib import Path
import pytest


# we use Path() so this works on Windows, Mac, and Linux automatically
REPO_ROOT = Path(__file__).parent.parent


INPUT_FILE = REPO_ROOT / "tests" / "fixtures" / "sample.fastq"
OUTPUT_DIR = REPO_ROOT / "tests" / "test_output"

def test_tool_runs_end_to_end():
    

    
    # Ensure the input file actually exists before we start
    assert INPUT_FILE.exists(), f"Missing test file! Please create: {INPUT_FILE}"

    # clean up any old output from previous runs so we know we are testing fresh
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    
    # This is equivalent to typing: python -m fastq_tool --input ... --output ...
    command = [
        sys.executable, "-m", "fastq_tool",
        "--input", str(INPUT_FILE),
        "--output", str(OUTPUT_DIR)
    ]

    
    # capture_output=True lets us see the error message if it crashes
    result = subprocess.run(command, capture_output=True, text=True)

    # 5. CHECK RESULTS (The "Gate")
    
    # check if the code crash (Exit code 0 means Success, 1 means Error)
    assert result.returncode == 0, f"Tool crashed! Error log:\n{result.stderr}"

    # check if is there a directory created
    assert OUTPUT_DIR.exists(), f"Output directory {OUTPUT_DIR} was not created."

    # check c if there is the result out?
    expected_files = ["qc.tsv", "run.json"]
    for filename in expected_files:
        file_path = OUTPUT_DIR / filename
        assert file_path.exists(), f"Missing output file: {filename}"