import pytest
from qc_tools.read import read_fastq, read_records, read_samples_tsv

def test_fastq_valid(tmp_path): #use dummy to chekc the if the script read and convert data correctly 
   
    f = tmp_path / "data.fq"
    f.write_text("@r1\nACGT\n+\nIIII\n")

    records = list(read_fastq(f))

    assert len(records) == 1
    assert records[0].seq_id == "r1"
    # check the converison of the fastq file, eg 'I' is ASCII 73, so 73-33=40
    assert records[0].qualities == [40, 40, 40, 40]

def test_fastq_filter(tmp_path):
    f = tmp_path / "messy.fq"

    content = (
        "@r1\nACGT\n+\nIIII\n" #good read dummy
        "@r2\nACGT\n+\nI\n"# mismatch dummy
        "@r3\nACZG\n+\nIIII\n"# bad characters dummy
    )
    f.write_text(content)

    records = list(read_fastq(f))

    # the funcctional script should skip r2 and r3
    assert len(records) == 1
    assert records[0].seq_id == "r1"

def test_read_records(tmp_path):# check if the files get passed to the correct parser
    fa = tmp_path / "test.fasta"
    fa.write_text(">s1\nATCG")
    assert list(read_records(fa))[0].qualities is None

    
    fq = tmp_path / "test.fastq"
    fq.write_text("@s1\nATCG\n+\nIIII")
    assert list(read_records(fq))[0].qualities is not None

def test_samples_tsv(tmp_path): #
    f = tmp_path / "samples.tsv"
    f.write_text("sample_id\tpath\tbatch\nS1\tdata/A.fq\tB1\n")
    
    data = read_samples_tsv(f)
    assert data[0] == ("S1", "data/A.fq", "B1")

def test_samples_tsv_error(tmp_path):#check input tsv
    f = tmp_path / "bad.tsv"
    f.write_text("id\tfile\nS1\tA.fq\n") # wrong headers

    with pytest.raises(ValueError):
        read_samples_tsv(f)