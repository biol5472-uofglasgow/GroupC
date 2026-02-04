from __future__ import annotations

from typing import Any, Dict, Iterable, Sequence

from qc_tools.read import Record

VALID_BASES = set("ACGTN")


def validate_sequence(seq: str) -> str:
    if seq is None:
        raise ValueError("Sequence is None")

    
    seq = seq.strip().upper()

    if len(seq) == 0:
        raise ValueError("Empty sequence")

    bad = set(seq) - VALID_BASES
    if bad:
        
        raise ValueError(
            f"Invalid bases found: {sorted(bad)!r} in sequence {seq!r}"
        )

    return seq



def seq_length(seq: str) -> int:
    # keep for backward compatibility
    
    seq = validate_sequence(seq)
    return len(seq)


def gc_fraction(seq: str) -> float:
    seq = validate_sequence(seq)
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)


def n_fraction(seq: str) -> float:
    seq = validate_sequence(seq)
    return seq.count("N") / len(seq)


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


def summarise_records(records: Iterable[Record]) -> Dict[str, Any]:
# running counters 
    n = 0
    total_bases = 0
    sum_gc = 0.0
    sum_n = 0.0
    
    # Quality counters
    sum_mean_qual = 0.0
    sum_q30 = 0.0
    has_qual = False

    for r in records:
        n += 1
        seq = validate_sequence(r.sequence)
        L = len(seq)

        total_bases += L
        sum_gc += gc_fraction(seq)
        sum_n += n_fraction(seq)

        if r.qualities is not None:
            has_qual = True
            sum_mean_qual += mean_quality(r.qualities)
            sum_q30 += q30_fraction(r.qualities)

    if n == 0:
        return {
            "n_seqs_or_reads": 0,
            "total_bases": 0,
            "mean_len": 0,
            "gc_fraction": 0,
            "n_fraction": 0,
        }

    out: Dict[str, Any] = {
        "n_seqs_or_reads": n,
        "total_bases": total_bases,
        "mean_len": total_bases/n,
        "gc_fraction": sum_gc / n,
        "n_fraction": sum_n / n,
    }

    if has_qual:
        out["mean_qual"] = sum_mean_qual / n
        out["q30_fraction"] = sum_q30 / n

    return out

