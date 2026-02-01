from typing import Iterator
from Bio import SeqIO
from dataclasses import dataclass
from typing import Optional, List, Tuple
import os
import csv
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]
import pyfastx

@dataclass
class Record:
    seq_id: str
    sequence: str
    qualities: Optional[List[int]]  # FASTA = None, FASTQ = [phred...]
    def __str__(self) -> str:
        return f"{self.seq_id}\t{self.sequence}\t{self.qualities}"

def read_fasta(path: str | Path) -> Iterator[Record]:
    try:
        for rec in SeqIO.parse(path, "fasta"):
            yield Record(
                seq_id=rec.id,
                sequence=str(rec.seq).upper(),
                qualities=None
            )
    except Exception as e:
        raise ValueError(f"Failed to read FASTA file: {path}") from e


def read_fastq(path: str | Path) -> Iterator[Record]:
    try:
        fq = pyfastx.Fastq(str(path))
        for r in fq:
            name = r.name
            seq = r.seq.upper()
            qual = r.qual
            if qual is None:
                print(f"Skipping invalid read {name}: missing quality")
                continue

            if len(seq) != len(qual):
                print(
                    f"Skipping invalid read {name}: "
                    f"sequence/quality length mismatch "
                    f"({len(seq)} vs {len(qual)})"
                )
                continue

            qualities = [ord(c) - 33 for c in qual]

            yield Record(
                seq_id=name,
                sequence=seq,
                qualities=qualities
            )

    except Exception as e:
        raise ValueError(f"Failed to read FASTQ file: {path}") from e

def read_records(path: str | Path):
    ext = os.path.splitext(path)[1].lower()
    if ext in [".fa", ".fasta", ".fna"]:
        return read_fasta(path)
    elif ext in [".fq", ".fastq"]:
        return read_fastq(path)
    else:
        raise ValueError(f"Unsupported file format: {path}")

def read_samples_tsv(path: str | Path) -> List[Tuple[str, str,str]]:
    samples = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        required = {"sample_id", "path", "batch"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(
                "samples.tsv must contain columns: sample_id, path, batch"
            )
        for row in reader:
            samples.append((row["sample_id"], row["path"],row["batch"]))
    return samples

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parents[2]
    data_file = BASE_DIR / "data" / "sampleB.fastq"
    for fas in read_fastq(data_file):
        print(fas)