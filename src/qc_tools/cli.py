import argparse
import json
import datetime
import pyfastx
from pathlib import Path

from .read import read_records
from .metrics import summarise_records


def main():
    parser = argparse.ArgumentParser(description="qc_tools cli (single input mode)")
    parser.add_argument("input", help="Input FASTA/FASTQ file")
    parser.add_argument("--outdir", default="result", help="Output directory")

    args = parser.parse_args()

    in_path = Path(args.input)
    out_dir = Path(args.outdir)

    if not in_path.exists():
        raise FileNotFoundError(f"input file not found: {in_path}")

    out_dir.mkdir(parents=True, exist_ok=True)

    # write run metadata
    run_info = {
    "tool": "qc_tools",
    "tool_version": "0.1.0",
    "input": str(in_path),
    "outdir": str(out_dir),
    "time": datetime.datetime.now().isoformat()
}
    (out_dir / "run.json").write_text(
        json.dumps(run_info, indent=2),
        encoding="utf-8"
    )

    # run qc
    records = read_records(in_path)
    summary = summarise_records(records)
    if in_path.suffix.lower() in [".fq", ".fastq"] and summary.get("n_seqs_or_reads", 0) == 0:
        fq = pyfastx.Fastq(str(in_path))
        comp = fq.composition or {}

        summary = {
            "n_seqs_or_reads": 0,         
            "total_bases": int(getattr(fq, "size", 0)),
            "mean_len": float(getattr(fq, "avglen", 0)),
            "gc_fraction": float(getattr(fq, "gc_content", 0)),
            "n_fraction": (comp.get("N", 0) / getattr(fq, "size", 1)) if getattr(fq, "size", 0) else 0,
            "fallback_mode": "pyfastx_file_level",
        }


    # add basic identifiers 
    summary["sample_id"] = in_path.stem
    summary["batch"] = "NA"

    # write qc.tsv 
    keys = sorted(summary.keys())
    qc_path = out_dir / "qc.tsv"
    with qc_path.open("w", encoding="utf-8") as f:
        f.write("\t".join(keys) + "\n")
        f.write("\t".join(str(summary[k]) for k in keys) + "\n")
        # write simple HTML report
    from .html_report import tsv_to_html
    html_path = out_dir / f"{in_path.stem}.html"
    tsv_to_html(qc_path, html_path, title=in_path.name)


    print("done:", str(qc_path))


if __name__ == "__main__":
    main()
