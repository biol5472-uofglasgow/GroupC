import pytest
from pytest import approx

from qc_tools.metrics import (
    seq_length,
    gc_fraction,
    n_fraction,
    mean_quality,
    q30_fraction,
    summarise_records,
)
from qc_tools.read import Record


def test_seq_length_normal():
    assert seq_length("ACGT") == 4


def test_seq_length_empty_raises():
    with pytest.raises(ValueError):
        seq_length("")


def test_gc_fraction_basic():
    assert gc_fraction("ACGT") == approx(0.5)


def test_gc_fraction_with_n():
    assert gc_fraction("ACNN") == approx(0.25)


def test_gc_fraction_invalid_base_raises():
    with pytest.raises(ValueError):
        gc_fraction("ACGTX")


def test_n_fraction_basic():
    assert n_fraction("ACNN") == approx(0.5)


def test_mean_quality_basic():
    assert mean_quality([30, 30, 40, 10]) == approx(27.5)


def test_q30_fraction_basic():
    assert q30_fraction([29, 30, 40, 10]) == approx(0.5)


def test_mean_quality_none_raises():
    with pytest.raises(ValueError):
        mean_quality(None)


def test_q30_fraction_empty_raises():
    with pytest.raises(ValueError):
        q30_fraction([])


def test_summarise_records_fasta():
    records = [
        Record("r1", "ACGT", None),
        Record("r2", "AANN", None),
    ]
    out = summarise_records(records)

    assert out["n_seqs_or_reads"] == 2
    assert out["total_bases"] == 8
    assert out["mean_len"] == approx(4.0)
    assert out["gc_fraction"] == approx((0.5 + 0.0) / 2)
    assert out["n_fraction"] == approx((0.0 + 0.5) / 2)
    assert "mean_qual" not in out
    assert "q30_fraction" not in out


def test_summarise_records_fastq():
    records = [
        Record("r1", "ACGT", [30, 30, 30, 30]),
        Record("r2", "GGGG", [40, 40, 20, 20]),
    ]
    out = summarise_records(records)

    assert out["n_seqs_or_reads"] == 2
    assert out["total_bases"] == 8
    assert "mean_qual" in out
    assert "q30_fraction" in out
