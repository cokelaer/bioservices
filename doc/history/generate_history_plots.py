"""
generate_history_plots.py
=========================

Generate figures that illustrate the evolution of the BioServices project
from its first commit (November 2012) to the present day.

Usage
-----
Run from the **root** of the bioservices repository::

    python doc/history/generate_history_plots.py

The script writes the following PNG files into ``doc/history/``:

* ``commits_over_time.png``     – monthly commit-activity bar chart
* ``contributors_over_time.png``– cumulative unique contributors
* ``services_timeline.png``     – Gantt-style timeline of service modules
* ``releases_timeline.png``     – release / version milestone timeline
* ``codebase_growth.png``       – lines-of-code growth (sampled at each tag)

Requirements
------------
matplotlib >= 3.5, numpy, pandas (all are runtime or dev dependencies of
bioservices already).
"""

import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")          # non-interactive backend — works in CI / headless
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR   = Path(__file__).resolve().parent        # doc/history/

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(cmd: str) -> str:
    """Run a shell command inside the repo and return stdout."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=REPO_ROOT
    )
    return result.stdout.strip()


def _save(fig: plt.Figure, name: str) -> None:
    path = OUT_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Wrote {path}")


# ---------------------------------------------------------------------------
# 1.  Commits over time (monthly bar chart + 6-month rolling average)
# ---------------------------------------------------------------------------

def plot_commits_over_time() -> None:
    raw = _run(
        "git log --format='%ai' --no-merges"
    )
    if not raw:
        print("  [warn] no git log output – skipping commits_over_time")
        return

    dates = pd.to_datetime(
        [line.strip()[:10] for line in raw.splitlines() if line.strip()],
        errors="coerce",
    ).dropna()
    series = (
        pd.Series(1, index=dates)
        .resample("ME")
        .sum()
        .fillna(0)
    )
    rolling = series.rolling(6, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.bar(series.index, series.values, width=20, color="#4C72B0",
           alpha=0.55, label="Monthly commits")
    ax.plot(rolling.index, rolling.values, color="#DD8452",
            linewidth=2, label="6-month rolling avg")

    # Shade development eras
    eras = [
        ("2012-11", "2014-12", "#AEC6CF", "Early development\n(v0.x–1.4)"),
        ("2015-01", "2019-12", "#B5EAD7", "Stable growth\n(v1.4–1.6)"),
        ("2020-01", "2022-12", "#FFDAC1", "API modernisation\n(v1.7–1.11)"),
        ("2023-01", "2026-06", "#C7CEEA", "Maintenance &\nAI-assisted (v1.12+)"),
    ]
    ymax = series.max() * 1.15
    for start, end, color, label in eras:
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end),
                   alpha=0.25, color=color, label=label)

    ax.set_xlim(pd.Timestamp("2012-10"), pd.Timestamp("2026-06"))
    ax.set_ylim(0, ymax)
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Number of commits", fontsize=11)
    ax.set_title("BioServices – Commit Activity over Time (non-merge commits)",
                 fontsize=13, fontweight="bold")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="upper left", fontsize=8, ncol=2)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    _save(fig, "commits_over_time.png")


# ---------------------------------------------------------------------------
# 2.  Cumulative unique contributors over time
# ---------------------------------------------------------------------------

def plot_contributors_over_time() -> None:
    raw = _run("git log --format='%ai|%an' --no-merges")
    if not raw:
        print("  [warn] no git log output – skipping contributors_over_time")
        return

    rows = []
    for line in raw.splitlines():
        parts = line.split("|", 1)
        if len(parts) == 2:
            rows.append({"date": parts[0][:10], "author": parts[1].strip()})

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date")

    # cumulative unique authors
    seen: set = set()
    dates_seen: list = []
    counts: list = []
    for _, row in df.iterrows():
        seen.add(row["author"])
        dates_seen.append(row["date"])
        counts.append(len(seen))

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.step(dates_seen, counts, where="post", color="#2ca02c", linewidth=2)
    ax.fill_between(dates_seen, counts, step="post", alpha=0.15, color="#2ca02c")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Cumulative unique contributors", fontsize=11)
    ax.set_title("BioServices – Growth in Unique Contributors",
                 fontsize=13, fontweight="bold")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlim(pd.Timestamp("2012-10"), pd.Timestamp("2026-06"))
    ax.grid(alpha=0.3)
    ax.annotate(
        f"Total: {len(seen)} contributors",
        xy=(0.98, 0.07), xycoords="axes fraction",
        ha="right", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="grey", alpha=0.8),
    )
    fig.tight_layout()
    _save(fig, "contributors_over_time.png")


# ---------------------------------------------------------------------------
# 3.  Services / modules timeline (Gantt-style)
# ---------------------------------------------------------------------------

# Manually curated service info: (module, category, added_year, deprecated_year|None)
_SERVICES = [
    # Core
    ("services.py",       "Core",          2012, None),
    ("settings.py",       "Core",          2012, None),
    ("xmltools.py",       "Core",          2012, None),
    # Sequence / Annotation
    ("uniprot.py",        "Sequence",      2012, None),
    ("kegg.py",           "Pathway",       2012, None),
    ("ncbiblast.py",      "Sequence",      2012, None),
    ("muscle.py",         "Sequence",      2012, None),
    ("eutils.py",         "Literature",    2012, None),
    ("chebi.py",          "Chemistry",     2013, None),
    ("biomart.py",        "Genomics",      2013, None),
    ("quickgo.py",        "Annotation",    2013, None),
    ("reactome.py",       "Pathway",       2013, None),
    ("arrayexpress.py",   "Genomics",      2013, None),
    ("wikipathway.py",    "Pathway",       2013, None),
    ("pathwaycommons.py", "Pathway",       2013, None),
    ("biomodels.py",      "Modelling",     2013, None),
    ("biodbnet.py",       "ID Mapping",    2013, None),
    ("psicquic.py",       "Interaction",   2013, None),
    ("miriam.py",         "Annotation",    2013, 2020),
    ("chembl.py",         "Chemistry",     2013, None),
    ("pdb.py",            "Structure",     2013, None),
    ("rhea.py",           "Chemistry",     2013, None),
    ("hgnc.py",           "Genomics",      2013, None),
    ("pfam.py",           "Sequence",      2013, None),
    ("ensembl.py",        "Genomics",      2014, None),
    ("eva.py",            "Genomics",      2015, None),
    ("intact.py",         "Interaction",   2015, None),
    ("pride.py",          "Proteomics",    2015, None),
    ("pubchem.py",        "Chemistry",     2016, None),
    ("ena.py",            "Sequence",      2016, None),
    ("omnipath.py",       "Signalling",    2016, None),
    ("chemspider.py",     "Chemistry",     2013, 2021),
    ("picr.py",           "ID Mapping",    2013, 2021),
    ("clinvitae.py",      "Clinical",      2014, 2021),
    ("omicsdi.py",        "Multi-omics",   2020, None),
    ("mygeneinfo.py",     "Genomics",      2020, None),
    ("pdbe.py",           "Structure",     2020, None),
    ("bigg.py",           "Modelling",     2020, None),
    ("util.py",           "Core",          2020, None),
    ("cog.py",            "Annotation",    2021, None),
    ("panther.py",        "Annotation",    2021, None),
    ("biocontainers.py",  "Infrastructure",2022, None),
    ("unichem.py",        "Chemistry",     2013, None),
    ("proteins.py",       "Proteomics",    2026, None),
]

_CATEGORY_COLORS = {
    "Core":           "#4C72B0",
    "Sequence":       "#55A868",
    "Pathway":        "#C44E52",
    "Genomics":       "#8172B2",
    "Chemistry":      "#CCB974",
    "Literature":     "#64B5CD",
    "Annotation":     "#DD8452",
    "Proteomics":     "#4ECDC4",
    "Structure":      "#1A535C",
    "Interaction":    "#FF6B6B",
    "Modelling":      "#A8DADC",
    "ID Mapping":     "#457B9D",
    "Signalling":     "#E07A5F",
    "Multi-omics":    "#3D405B",
    "Clinical":       "#81B29A",
    "Infrastructure": "#F2CC8F",
}

END_YEAR = 2026


def plot_services_timeline() -> None:
    # Sort by category then added year
    services = sorted(_SERVICES, key=lambda x: (x[1], x[2]))
    categories = sorted(set(s[1] for s in services))

    fig_height = max(6, len(services) * 0.32)
    fig, ax = plt.subplots(figsize=(13, fig_height))

    yticks, ylabels = [], []
    for i, (name, cat, added, depr) in enumerate(services):
        color = _CATEGORY_COLORS.get(cat, "#888888")
        end = depr if depr else END_YEAR + 0.5
        alpha = 0.4 if depr else 0.85
        ax.barh(i, end - added, left=added, height=0.65,
                color=color, alpha=alpha, edgecolor="white", linewidth=0.5)
        if depr:
            ax.text(end + 0.05, i, "✕", va="center", fontsize=7, color="#888")
        yticks.append(i)
        ylabels.append(name.replace(".py", ""))

    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels, fontsize=7.5)
    ax.set_xlabel("Year", fontsize=11)
    ax.set_title("BioServices – Service Modules Timeline",
                 fontsize=13, fontweight="bold")
    ax.set_xlim(2012, END_YEAR + 1)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str(int(x))))
    ax.grid(axis="x", alpha=0.3)
    ax.invert_yaxis()

    # Legend for categories
    legend_patches = [
        mpatches.Patch(color=_CATEGORY_COLORS[c], label=c, alpha=0.85)
        for c in categories if c in _CATEGORY_COLORS
    ]
    ax.legend(handles=legend_patches, loc="lower right",
              fontsize=7, ncol=2, title="Category")
    fig.tight_layout()
    _save(fig, "services_timeline.png")


# ---------------------------------------------------------------------------
# 4.  Release / version milestone timeline
# ---------------------------------------------------------------------------

_RELEASES = [
    ("v0.13",  2013,  2, "First PyPI release\n(KEGG, UniProt, ChEMBL…)"),
    ("v1.4.0", 2015, 10, "TCGA, PRIDE,\nEVA added"),
    ("v1.5",   2016,  1, "ENA, PubChem,\nOmniPath added"),
    ("v1.6",   2017,  6, "ChEMBL API v2,\nQuickGO rewrite"),
    ("v1.7.0", 2020,  2, "Panther, reorg,\ndrop Py2"),
    ("v1.7.4", 2020,  3, "BioModels REST API\n(COMBINE hackathon)"),
    ("v1.7.12",2021,  7, "COG, MyGeneInfo,\nPDBe added"),
    ("v1.8.0", 2021,  9, "Removed deprecated\nservices (ChemSpider…)"),
    ("v1.9.0", 2022,  5, "BioContainers,\npackaging overhaul"),
    ("v1.10.0",2022,  7, "Minor API fixes\n& new methods"),
    ("v1.11.0",2022, 12, "Stability & tests"),
    ("v1.12.0",2025,  1, "Poetry / pyproject,\nCI modernisation"),
    ("v1.14.0",2026,  3, "EBI Proteins,\nAI-assisted fixes"),
]


def plot_releases_timeline() -> None:
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(2012.5, 2026.8)
    ax.set_ylim(-1.5, 2.5)
    ax.axhline(0, color="#333", linewidth=1.5, zorder=0)
    ax.set_yticks([])
    ax.set_xlabel("Year", fontsize=11)
    ax.set_title("BioServices – Release Milestones",
                 fontsize=13, fontweight="bold")

    for idx, (ver, year, month, note) in enumerate(_RELEASES):
        x = year + (month - 1) / 12.0
        above = (idx % 2 == 0)
        ybase = 0.05 if above else -0.05
        ytip  = 1.3 if above else -1.3
        ax.annotate(
            "",
            xy=(x, ybase), xytext=(x, ytip),
            arrowprops=dict(arrowstyle="-", color="#777", lw=1.0),
        )
        ax.plot(x, 0, "o", ms=8, color="#4C72B0", zorder=5)
        ax.text(
            x, ytip + (0.1 if above else -0.1),
            f"{ver}\n{note}",
            ha="center", va="bottom" if above else "top",
            fontsize=7.5,
            bbox=dict(boxstyle="round,pad=0.25", fc="white",
                      ec="#4C72B0", alpha=0.9, linewidth=0.8),
        )

    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str(int(x))))
    ax.grid(axis="x", alpha=0.2)
    ax.tick_params(axis="x", labelsize=9)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    fig.tight_layout()
    _save(fig, "releases_timeline.png")


# ---------------------------------------------------------------------------
# 5.  Codebase growth (lines of code at each tagged release)
# ---------------------------------------------------------------------------

def _count_py_lines(ref: str) -> int:
    """Return total Python LOC at a given git ref."""
    raw = _run(
        f"git show {ref}:src/bioservices/__init__.py 2>/dev/null | wc -l"
    )
    # Lightweight proxy: count all .py lines in the tree at that ref
    result = subprocess.run(
        f"git ls-tree -r --name-only {ref} | grep '\\.py$' | "
        f"xargs -I{{}} git show {ref}:{{}} 2>/dev/null | wc -l",
        shell=True, capture_output=True, text=True, cwd=REPO_ROOT
    )
    try:
        return int(result.stdout.strip())
    except ValueError:
        return 0


def plot_codebase_growth() -> None:
    raw_tags = _run("git tag --sort=version:refname")
    tags = [t for t in raw_tags.splitlines() if t.strip()]

    records = []
    for tag in tags:
        date_str = _run(f"git log -1 --format='%ai' {tag}").strip()[:10]
        if not date_str:
            continue
        loc = _count_py_lines(tag)
        if loc > 0:
            records.append({"tag": tag, "date": date_str, "loc": loc})

    if not records:
        print("  [warn] no LOC data – skipping codebase_growth")
        return

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Also sample HEAD
    head_loc = _count_py_lines("HEAD")
    head_row = pd.DataFrame([{"tag": "HEAD", "date": pd.Timestamp("today"),
                               "loc": head_loc}])
    df = pd.concat([df, head_row], ignore_index=True)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.fill_between(df["date"], df["loc"], alpha=0.25, color="#4C72B0")
    ax.plot(df["date"], df["loc"], "o-", color="#4C72B0",
            linewidth=2, markersize=6)

    for _, row in df[df["tag"] != "HEAD"].iterrows():
        ax.annotate(
            row["tag"],
            xy=(row["date"], row["loc"]),
            xytext=(0, 8), textcoords="offset points",
            ha="center", fontsize=6.5, rotation=45,
            color="#333",
        )

    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Total Python lines of code", fontsize=11)
    ax.set_title("BioServices – Codebase Growth (Python LOC at each release)",
                 fontsize=13, fontweight="bold")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{int(x):,}")
    )
    ax.grid(alpha=0.3)
    fig.tight_layout()
    _save(fig, "codebase_growth.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("BioServices – generating history plots …")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    plot_commits_over_time()
    plot_contributors_over_time()
    plot_services_timeline()
    plot_releases_timeline()
    plot_codebase_growth()

    print("Done.  All figures written to", OUT_DIR)


if __name__ == "__main__":
    main()
