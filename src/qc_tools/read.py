from typing import Iterator
from Bio import SeqIO
from dataclasses import dataclass
from typing import Optional, List, Tuple
import os
import csv
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]

@dataclass
class Record:
    seq_id: str
    sequence: str
    qualities: Optional[List[int]]  # FASTA = None, FASTQ = [phred...]
    def __str__(self) -> str:
        return f"{self.seq_id}\t{self.sequence}\t{self.qualities}"

def read_fasta(path: str) -> Iterator[Record]:
    try:
        for rec in SeqIO.parse(path, "fasta"):
            yield Record(
                seq_id=rec.id,
                sequence=str(rec.seq).upper(),
                qualities=None
            )
    except Exception as e:
        raise ValueError(f"Failed to read FASTA file: {path}") from e

def read_fastq(path: str) -> Iterator[Record]:
    try:
        for rec in SeqIO.parse(path, "fastq"):
            seq = str(rec.seq).upper()
            quals = rec.letter_annotations.get("phred_quality")

            if quals is None:
                raise ValueError(f"Missing quality scores in FASTQ: {rec.id}")
            if len(seq) != len(quals):
                raise ValueError(
                    f"Sequence/quality length mismatch in {rec.id}"
                )

            yield Record(
                seq_id=rec.id,
                sequence=seq,
                qualities=quals
            )
    except Exception as e:
        raise ValueError(f"Failed to read FASTQ file: {path}") from e


def read_records(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext in [".fa", ".fasta", ".fna"]:
        return read_fasta(path)
    elif ext in [".fq", ".fastq"]:
        return read_fastq(path)
    else:
        raise ValueError(f"Unsupported file format: {path}")

def read_samples_tsv(path: str) -> List[Tuple[str, str,str]]:
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
    data_file = BASE_DIR / "data" / "sampleA.fastq"
    sample_file = BASE_DIR / "samples.tsv"
    for fas in read_records(data_file):
        print(fas)
    for sam in read_samples_tsv(sample_file):
        print(sam)