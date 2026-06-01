# Figure Provenance

| Figure | Source | Command |
|--------|--------|---------|
| `mega_suite_duration_p10.png` | manifest + sobol | `python analysis/generate_figures.py` |
| `duration_sensitivity.png` | manifest + sobol | `python analysis/generate_figures.py` |
| `form_factor/*.png` | form_factor.yaml + params.yaml | `python analysis/generate_form_factor_assets.py` |
| `form_factor/renders/*.png` | render_mesh + form_factor.yaml | `python analysis/generate_3d_renders.py` |
