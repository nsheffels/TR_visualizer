"""Build the shareable web version of the TR pathogenicity visualizer.

    python build_site.py

Reads the notebook's table-building cell (section 1 of TR_pathogenicity_visualizer.ipynb)
straight out of the .ipynb and runs it, so the web page always uses exactly the same matching,
evidence filtering and cohort statistics as the notebook. The resulting per-locus table is
embedded into web/template.html and written to index.html, which GitHub Pages serves.

Re-run this whenever the notebook's data-building code or anything in data/ changes, then
commit index.html.

Needs only: pandas, numpy (the same as the notebook's section 1).
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "TR_pathogenicity_visualizer.ipynb"
TEMPLATE = ROOT / "web" / "template.html"
OUTPUT = ROOT / "index.html"
PLACEHOLDER = "/*__TR_DATA__*/null"
BUILD_CELL_MARKER = "def build_disease_df("


def load_build_cell():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    for cell in nb["cells"]:
        src = "".join(cell["source"])
        if cell["cell_type"] == "code" and BUILD_CELL_MARKER in src:
            return src
    raise SystemExit(f"Couldn't find the cell containing {BUILD_CELL_MARKER!r} in {NOTEBOOK.name}")


def clean(v):
    """JSON-safe scalar: NaN/inf -> None, numpy types -> Python types."""
    if v is None:
        return None
    if hasattr(v, "item"):
        v = v.item()
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v


def main():
    import re
    import numpy as np
    import pandas as pd

    ns = {"json": json, "re": re, "math": math, "np": np, "pd": pd,
          "Path": Path, "DATA_DIR": ROOT / "data"}
    exec(compile(load_build_cell(), "notebook:section1", "exec"), ns)
    df = ns["df"]
    cohorts = ns["COHORT_KEYS"]

    keep = ["dataset", "gene", "disease", "disease_id", "locus_id", "motif", "motif_len_bp",
            "ref_repeats", "region_catalog", "region_class", "region_strchive", "inheritance",
            "evidence", "benign_max", "intermediate_min", "intermediate_max",
            "pathogenic_min", "pathogenic_max"]
    records = []
    for _, r in df.iterrows():
        rec = {k: clean(r[k]) if not isinstance(r[k], (list, tuple)) else list(r[k]) for k in keep}
        rec["cohort_stats"] = {
            c: {k: clean(v) for k, v in s.items()} for c, s in (r["cohort_stats"] or {}).items()
        }
        records.append(rec)

    payload = {"cohorts": cohorts, "loci": records}
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise SystemExit(f"{TEMPLATE} is missing the data placeholder {PLACEHOLDER!r}")
    data_js = json.dumps(payload, separators=(",", ":")).replace("</", "<\\/")
    OUTPUT.write_text(template.replace(PLACEHOLDER, data_js), encoding="utf-8")

    n_dis = sum(r["dataset"] == "disease" for r in records)
    print(f"Wrote {OUTPUT.name}: {n_dis} disease loci, {len(records) - n_dis} background loci.")


if __name__ == "__main__":
    main()
