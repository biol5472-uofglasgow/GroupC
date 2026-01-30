from qc_tools.read import read_fasta

def test_read_records(tmp_path):
    fasta = tmp_path / "test.fasta"
    fasta.write_text(
        ">seq1\n"
        "ATCG\n"
        ">seq2\n"
        "GGTT\n"
    )

    records = list(read_fasta(str(fasta)))

    assert len(records) == 2

    assert records[0].seq_id == "seq1"
    assert records[0].sequence == "ATCG"
    assert records[0].qualities is None

    assert records[1].seq_id == "seq2"
    assert records[1].sequence == "GGTT"
    assert records[1].qualities is None

