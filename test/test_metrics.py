import pytest
from src.metrics import seq_length


def test_seq_length_normal():
    assert seq_length("ACGT") == 4


def test_seq_length_empty_raises():
    with pytest.raises(ValueError):
        seq_length("")
#test_gc-fraction
from pytest import approx
from src.metrics import gc_fraction


def test_gc_fraction_basic():
    assert gc_fraction("ACGT") == approx(0.5)


def test_gc_fraction_with_n():
    assert gc_fraction("ACNN") == approx(0.25)


def test_gc_fraction_invalid_base_raises():
    import pytest
    with pytest.raises(ValueError):
        gc_fraction("ACGTX")
#test_n_fraction
from src.metrics import n_fraction


def test_n_fraction_basic():
    assert n_fraction("ACNN") == approx(0.5)
#test_fastq
from src.metrics import mean_quality, q30_fraction


def test_mean_quality_basic():
    assert mean_quality([30, 30, 40, 10]) == approx(27.5)


def test_q30_fraction_basic():
    assert q30_fraction([29, 30, 40, 10]) == approx(0.5)


def test_quality_none_raises():
    import pytest
    with pytest.raises(ValueError):
        mean_quality(None)


def test_quality_empty_raises():
    import pytest
    with pytest.raises(ValueError):
        q30_fraction([])

