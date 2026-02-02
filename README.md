# FASTA/FASTQ QC CLI Tool

A simple command-line tool for computing basic QC metrics from FASTA or FASTQ files.

The tool focuses on **CLI usage**, supports **strict read-level QC**, and provides a **fallback summary** for malformed FASTQ inputs. A minimal **HTML report** is also generated for each run.

---

## Requirements

- Python ≥ 3.9
- Biopython
- pyfastx

```bash
pip install biopython pyfastx
```

---

## Usage

Run QC on a FASTA or FASTQ file:

```bash
python -m qc_tools.cli input.fastq --outdir results
```

Show help:

```bash
python -m qc_tools.cli --help
```

---

## Output

Each run produces the following files in the output directory:

### `qc.tsv`

A tab-separated summary of QC metrics, including:

- `n_seqs_or_reads`
- `total_bases`
- `mean_len`
- `gc_fraction`
- `n_fraction`

For FASTQ input, quality metrics are included when available:

- `mean_qual`
- `q30_fraction`

If no valid reads remain after strict QC, the tool falls back to file-level statistics. This behaviour is explicitly marked using the `fallback_mode` field.

---

### `run.json`

Records basic run metadata (input, output directory, timestamp).

---

### `sampleX.html`

A simple HTML report generated from `qc.tsv` for quick inspection of results.

---

## Notes

This tool was developed as part of a coursework assignment emphasising robust CLI design and handling of malformed FASTA/FASTQ inputs.

