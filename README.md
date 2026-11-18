# TR pathogenicity visualizer

**Use it in your browser, with no install and no account:**
**https://nsheffels.github.io/TR_visualizer/**

For known disease-associated tandem repeats, the visualizer plots how far each locus stretches in
ordinary population cohorts (max observed ÷ reference repeat count) against how much it varies
between people (population SD). A region-matched background sample of non-disease repeats is
available for comparison.

- **Plot 1:** one cohort at a time (HPRC256, TenK10K, AoU1027), colored by region class.
  You can download the current view as a CSV.
- **Plot 2:** cohorts compared on the same axes.
- Click any point for details. Drag or scroll to zoom, and double-click to reset.
AI use: The notebook and web version were developed with Claude (Anthropic; Claude Opus 4.5 notebook, Opus 5.5 web version),
2026-10 to 2026-11. The AI wrote code for data parsing, plotting, and the web page under my direction. I designed the analysis,
chose the data sources and filters, and verified the outputs against the source data.
## Running the notebook (for the full analysis code)

    pip install -r requirements.txt
    jupyter notebook TR_pathogenicity_visualizer.ipynb

If you get `module 'numpy' has no attribute 'bool8'`, your plotly is too old for numpy 2:
run `pip install -U plotly` and restart the kernel.

## How the web page is built

`build_site.py` runs the notebook's section-1 table-building cell directly from the `.ipynb`,
so the web page and the notebook always use the same matching and filtering. It embeds the
result in `web/template.html` and writes `index.html`. On every push to `main`, the GitHub Action
in `.github/workflows/pages.yml` runs that build and publishes the page.

To preview locally: `python build_site.py`, then open `index.html` in a browser.

## Contents

- `TR_pathogenicity_visualizer.ipynb`: the notebook
- `build_site.py`, `web/template.html`: the web version
- `data/TR_catalog_63loci.json`: the 63-locus disease catalog (gene, motif, reference repeats, region)
- `data/STRchive_loci.json`: [STRchive](https://github.com/dashnowlab/STRchive) disease thresholds,
  evidence tier, and inheritance
- `data/TRExplorer_disease_loci_full.json`: the same disease loci from the full
  [TRExplorer v2.0](https://github.com/broadinstitute/trexplorer-catalog) catalog (per-cohort SD, max,
  99th percentile, n)
- `data/TRExplorer_matched_sample.json`: region- and motif-length-matched background loci
  (non-disease) from TRExplorer v2.0
- `current_view.csv`: written by the notebook's export cell
