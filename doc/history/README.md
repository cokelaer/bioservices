# BioServices – Project Evolution History

This directory contains materials that document the evolution of the
[BioServices](https://github.com/cokelaer/bioservices) project from its
first commit (November 2012) to the present.

## Contents

| File | Description |
|------|-------------|
| `generate_history_plots.py` | Script that reads the git history and generates all figures |
| `evolution_summary.rst` | Narrative summary suitable for inclusion in a paper (RST format) |
| `commits_over_time.png` | Monthly commit activity bar chart (2012–2026) |
| `contributors_over_time.png` | Cumulative unique contributors over time |
| `services_timeline.png` | Gantt-style timeline of service modules |
| `releases_timeline.png` | Annotated release milestone timeline |
| `codebase_growth.png` | Python lines-of-code growth at each tagged release |

## Regenerating the figures

Run the script from **any working directory** – it automatically locates the
repository root and writes figures to the `doc/history/` directory:

```bash
# from the repository root
python doc/history/generate_history_plots.py

# or from anywhere, using the full path
python /path/to/bioservices/doc/history/generate_history_plots.py
```

Dependencies (all already in `pyproject.toml`): `matplotlib >= 3.9`,
`numpy`, `pandas`.
