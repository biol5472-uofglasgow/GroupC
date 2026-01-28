from __future__ import annotations

from typing import Iterable, Sequence, Dict, Any
from src.read import Record
def seq_length(seq: str) -> int:
    if seq is None:
        raise ValueError("Sequence is None")
    if len(seq) == 0:
        raise ValueError("Empty sequence")
    return len(seq)
VALID_BASES = set("ACGTN")


def validate_sequence(seq: str) -> None:
    bad = set(seq) - VALID_BASES
    if bad:
        raise ValueError(f"Invalid bases found: {''.join(sorted(bad))}")


def gc_fraction(seq: str) -> float:
    seq = seq.upper()
    seq_length(seq)
    validate_sequence(seq)
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)
