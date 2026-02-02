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
    # keep for backward compatibility / explicitness
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
    n = 0
    total_bases = 0
    lengths: list[int] = []
    gcs: list[float] = []
    ns: list[float] = []
    mean_quals: list[float] = []
    q30s: list[float] = []

    for r in records:
        n += 1
        seq = validate_sequence(r.sequence)
        L = len(seq)

        total_bases += L
        lengths.append(L)
        gcs.append(gc_fraction(seq))
        ns.append(n_fraction(seq))

        if r.qualities is not None:
            mean_quals.append(mean_quality(r.qualities))
            q30s.append(q30_fraction(r.qualities))

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
        "mean_len": sum(lengths) / len(lengths),
        "gc_fraction": sum(gcs) / len(gcs),
        "n_fraction": sum(ns) / len(ns),
    }

    if mean_quals:
        out["mean_qual"] = sum(mean_quals) / len(mean_quals)
        out["q30_fraction"] = sum(q30s) / len(q30s)

    return out

