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

#summary
def q30_fraction(phred: Sequence[int]) -> float:
    if phred is None:
        raise ValueError("Qualities is None")
    if len(phred) == 0:
        raise ValueError("Empty qualities")
    return sum(1 for q in phred if q >= 30) / len(phred)


def summarise_records(records: Iterable[Record]) -> Dict[str, Any]:
    n = 0
    total_bases = 0
    lengths = []
    gcs = []
    ns = []
    mean_quals = []
    q30s = []

    for r in records:
        n += 1
        L = seq_length(r.sequence)
        total_bases += L
        lengths.append(L)
        gcs.append(gc_fraction(r.sequence))
        ns.append(n_fraction(r.sequence))

        if r.qualities is not None:
            mean_quals.append(mean_quality(r.qualities))
            q30s.append(q30_fraction(r.qualities))

    if n == 0:
        raise ValueError("No records found")

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


