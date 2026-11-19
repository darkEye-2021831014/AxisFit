#!/usr/bin/env python3
"""Pre-push check for this repository.

Verifies that
  1. every file the README promises is present (including the extended-analysis
     notebooks and results),
  2. every notebook parses (nbformat.validate + ast.parse) and has no stored outputs,
  3. no file exceeds GitHub's 100 MB hard limit (warns above 50 MB),
  4. no OS or archive clutter (.DS_Store, __MACOSX, *.zip) is present.

Run from the repository root:  python scripts/check_release.py
Needs:  pip install nbformat
"""
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
problems, warnings = [], []

REQUIRED = [
    "README.md", "LICENSE", "CITATION.cff", "requirements.txt", ".gitignore",
    "data/README.md", "docs/paper_to_files.md", "scripts/verify_paper_claims.py",
    "protocol/axis_configs.json", "protocol/axis_configs_extended.json",
    "protocol/loso_folds.json", "protocol/windows_index.parquet",
    "notebooks/00_data_audit.ipynb", "notebooks/01_classical_models.ipynb",
    "notebooks/02_cnn.ipynb", "notebooks/03_analysis.ipynb",
    "results/master_results.csv", "results/raw/classical_full/results.csv",
    "results/raw/cnn_full/results.csv",
    "results/figures/Fig01_pipeline.pdf", "results/figures/Fig02_sensor_positions.pdf",
] + [f"results/figures_extended/FX{i}_{n}.pdf" for i, n in [
    (1, "macroF1_heatmap_30_configs"), (2, "E1_E2_vs_6axis"),
    (3, "best_median_worst_by_channel_count"), (4, "pareto_f1_vs_data_rate"),
    (5, "pairs_by_type"), (6, "model_ranking_agreement"), (7, "seed_sd_by_channels"),
    (8, "systems_vs_channels"), (9, "complementarity_mixed_vs_pure"),
    (10, "perclass_mixAxGz"), (11, "selection_optimism")]]

# Extended-analysis material, copied in from the local working tree.
EXTENSION_REQUIRED = [
    "notebooks/04b_classical_seeds.ipynb", "notebooks/02_cnn_seeds43-46.ipynb",
    "notebooks/04c_seed_analysis.ipynb", "notebooks/05_latency_and_cost.ipynb",
    "notebooks/06_analysis_extended.ipynb",
    "results/tables_extended", "results/tables_seeds",
    "results/raw/extended_full", "results/raw/cnn_seeds43-46_full",
    "results/raw/classical_seed43", "results/raw/classical_seed44", "results/raw/latency_full",
]

for rel in REQUIRED:
    if not (ROOT / rel).exists():
        problems.append(f"missing: {rel}")
for rel in EXTENSION_REQUIRED:
    if not (ROOT / rel).exists():
        problems.append(f"missing extension material: {rel}")

try:
    import nbformat
except ImportError:
    nbformat = None
    warnings.append("nbformat not installed; notebooks were not validated")

for nb_path in sorted(ROOT.rglob("*.ipynb")):
    rel = nb_path.relative_to(ROOT)
    if ".ipynb_checkpoints" in nb_path.parts:
        problems.append(f"checkpoint folder present: {rel}")
        continue
    if nbformat is None:
        continue
    try:
        nb = nbformat.read(str(nb_path), as_version=4)
        nbformat.validate(nb)
    except Exception as exc:  # noqa: BLE001
        problems.append(f"{rel}: nbformat.validate failed: {exc}")
        continue
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        if cell.get("outputs"):
            problems.append(f"{rel}: cell {i} has stored outputs (strip them)")
        lines = [("pass" if l.lstrip().startswith(("%", "!")) else l) for l in cell.source.splitlines()]
        try:
            ast.parse("\n".join(lines))
        except SyntaxError as exc:
            problems.append(f"{rel}: cell {i} does not parse: {exc}")

for p in ROOT.rglob("*"):
    if not p.is_file():
        continue
    rel = p.relative_to(ROOT)
    size = p.stat().st_size
    if size > 100 * 1024 * 1024:
        problems.append(f"{rel}: {size/1e6:.0f} MB exceeds GitHub's 100 MB limit")
    elif size > 50 * 1024 * 1024:
        warnings.append(f"{rel}: {size/1e6:.0f} MB (GitHub warns above 50 MB)")
    if p.name == ".DS_Store" or "__MACOSX" in p.parts or p.suffix == ".zip":
        problems.append(f"clutter: {rel}")
    if p.name == "confusion_long.csv" or p.name == "pooled_confusion_long.csv":
        warnings.append(f"{rel}: confusion matrices are meant to stay out of Git (paper: available on request)")

for w in warnings:
    print("WARN  " + w)
for q in problems:
    print("FAIL  " + q)
print(f"\n{len(problems)} problem(s), {len(warnings)} warning(s)")
sys.exit(1 if problems else 0)
