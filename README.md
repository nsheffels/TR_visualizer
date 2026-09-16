# TR pathogenicity visualizer

Comparing Fold change and Z score to SD
## generated the visualizer with claude
## Setup

    pip install -r requirements.txt
    jupyter notebook TR_pathogenicity_visualizer.ipynb

(or open it in JupyterLab / VS Code's notebook UI.)

The plot is a plain `plotly.graph_objects.Figure`, redrawn and redisplayed on every
slider/toggle change, rather than a live-patched `FigureWidget` — slightly less smooth,
but it sidesteps a version-compatibility break (`AttributeError: type object 'DOMWidget'
has no attribute '_ipython_display_'`) that `FigureWidget` hits on some
ipywidgets/plotly/Jupyter combinations (Anaconda's bundled versions among them). If you
still see any widget-related error, updating ipywidgets and restarting the kernel
(`pip install -U ipywidgets`, then Kernel > Restart) usually clears it.


## Contents

- `TR_pathogenicity_visualizer.ipynb` — the notebook. Run all cells; controls appear
  under the plot.
- `data/TR_catalog_63loci.json` — uploaded 63-locus catalog from TR Explorer which were marked as overlapping a disease loci (population stats).
- `data/STRchive_loci.json` — STRchive's disease-threshold database (pathogenic/benign
  copy-number ranges), used to compute fold-change and z-score. 
  https://github.com/dashnowlab/STRchive 
- `current_view.csv` — written by the notebook's last cell, whatever is currently
  selected by the widgets.

