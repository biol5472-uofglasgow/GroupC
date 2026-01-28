import pytest
from src.metrics import seq_length


def test_seq_length_normal():
    assert seq_length("ACGT") == 4


def test_seq_length_empty_raises():
    with pytest.raises(ValueError):
        seq_length("")
