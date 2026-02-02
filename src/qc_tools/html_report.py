from __future__ import annotations
from pathlib import Path
import csv
import html
import datetime


def _read_tsv(tsv_path: Path) -> tuple[list[str], list[list[str]]]:
    with tsv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        rows = list(reader)
    if not rows:
        return [], []
    header = rows[0]
    data_rows = rows[1:] if len(rows) > 1 else []
    return header, data_rows


def tsv_to_html(tsv_path: str | Path, html_path: str | Path, title: str | None = None) -> None:
    tsv_path = Path(tsv_path)
    html_path = Path(html_path)
    header, rows = _read_tsv(tsv_path)

    page_title = title or tsv_path.stem
    now = datetime.datetime.now().isoformat(timespec="seconds")

    # build table html
    if not header:
        table_html = "<p>No data found in TSV.</p>"
    else:
        ths = "".join(f"<th>{html.escape(h)}</th>" for h in header)
        trs = []
        for r in rows:
            tds = "".join(f"<td>{html.escape(x)}</td>" for x in r)
            trs.append(f"<tr>{tds}</tr>")
        table_html = f"""
        <table>
          <thead><tr>{ths}</tr></thead>
          <tbody>
            {''.join(trs) if trs else '<tr><td colspan="' + str(len(header)) + '">No rows</td></tr>'}
          </tbody>
        </table>
        """

    doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(page_title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; }}
    h1 {{ margin-bottom: 6px; }}
    .meta {{ color: #555; margin-bottom: 16px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f5f5f5; }}
    tr:nth-child(even) {{ background: #fafafa; }}
    code {{ background: #f5f5f5; padding: 2px 4px; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>{html.escape(page_title)}</h1>
  <div class="meta">Generated: <code>{html.escape(now)}</code><br>
  Source: <code>{html.escape(str(tsv_path))}</code></div>
  {table_html}
</body>
</html>
"""
    html_path.write_text(doc, encoding="utf-8")
