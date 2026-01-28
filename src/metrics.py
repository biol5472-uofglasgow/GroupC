from __future__ import annotations

from typing import Iterable, Sequence, Dict, Any
from src.read import Record
def seq_length(seq: str) -> int:
    if seq is None:
        raise ValueError("Sequence is None")
    if len(seq) == 0:
        raise ValueError("Empty sequence")
    return len(seq)
