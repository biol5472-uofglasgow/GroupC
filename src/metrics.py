from __future__ import annotations

from typing import Iterable, Sequence, Dict, Any
from src.read import Record
def seq_length(seq: str) -> int:
    if seq is None:
        raise ValueError("Sequence is None")
    if len(seq) == 0:
        raise ValueError("Empty sequence")
    return len(seq)
#gc_fraction
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

#n_fraction
def n_fraction(seq: str) -> float:
    seq = seq.upper()
    seq_length(seq)
    validate_sequence(seq)
    return seq.count("N") / len(seq)
#fastq
def mean_quality(phred: Sequence[int]) -> float:
    if phred is None:
        raise ValueError("Qualities is None")
    if len(phred) == 0:
        raise ValueError("Empty qualities")
    return sum(phred) / len(phred)


def q30_fraction(phred: Sequence[int]) -> float:
    if phred is None:
        raise ValueError("Qualities is None")
    if len(phred) == 0:
        raise ValueError("Empty qualities")
    return sum(1 for q in phred if q >= 30) / len(phred)


