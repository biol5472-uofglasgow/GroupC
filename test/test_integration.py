import subprocess
import sys
from pathlib import Path

def test_cli_integration(tmp_path):#run tool from start to end
    
    
    input_file = tmp_path / "integration_test.fq"
    input_file.write_text("@r1\nACGT\n+\nIIII\n")# creating a fake input file 
    
    output_dir = tmp_path / "results"

    # running the scripts as a subprocess and using the cli
    # using sys.executable to ensure we use the same Python environment
    cmd = [
        sys.executable, "-m", "qc_tools.cli",  
        "--outdir", str(output_dir)
    ]
    
    # run the command and check it didn't crash (return code 0)
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Tool crashed! Error: {result.stderr}"

    # check if the output files were actually created
    assert (output_dir / "run.json").exists(), "run.json not created"
    assert (output_dir / "qc.tsv").exists(), "qc.tsv not created"
    
    # checking if the HTML report exists (based on the cli.py )
    # cli.py generates {stem}.html?
    assert (output_dir / "integration_test.html").exists(), "html report missing"

    # verfitying the output
    qc_content = (output_dir / "qc.tsv").read_text()
    assert "r1" in qc_content or "1" in qc_content  # Check if it counted the read