# Placement-Specific Axis Reduction of Wearable Inertial Sensors for Gym Exercise Recognition

Wearable inertial sensing supports gym exercise recognition, but every accelerometer and gyroscope axis adds sampling, transmission and storage cost, and it is unclear which axes are worth keeping. This repository contains the full analysis for a study that evaluated **15 axis configurations** — from the full six-axis set through every three-axis subset, sensor pair and single axis — on the public **RecGym** dataset at three body positions (wrist, pocket, calf). A random forest, support vector machine, gradient-boosted trees and a 1-D convolutional network were scored by macro-F1 under leave-one-subject-out validation (10 subjects, 12 labels, 105,728 windows). The headline finding is that axis-level reduction is a **placement-specific decision**, not a universal saving: the calf tolerated reduction best, the wrist least, and the accelerometer-minus-gyroscope gap reversed with placement.

This is the reproducibility repository for the paper *"Placement-Specific Axis Reduction of Wearable Inertial Sensors for Gym Exercise Recognition"* (IEEE Sensors Journal, under review).

---

## What is in this repository

| Path | Contents |
|---|---|
| `notebooks/` | The four analysis notebooks (`00` → `03`), outputs stripped |
| `protocol/` | Small JSON manifests that fix the protocol: axis configs, LOSO folds, label/position maps, subject list, audit summary, compute plan, window metadata and window index |
| `results/raw/classical_full/` | Raw per-fold output of notebook 01 (RF, SVM, XGB) |
| `results/raw/cnn_full/` | Raw per-fold output of notebook 02 (1-D CNN) |
| `results/tables/` | All paper and supplementary tables as CSV (31 files, indexed by `TABLES_INDEX.csv`) |
| `results/figures/` | All figures as PNG (13 files) |
| `results/analysis_checks/` | Integrity checks, analysis manifest, latency note and run log from notebook 03 |
| `results/master_results.csv` | Long-format master table of all per-cell results |
| `results/master_results_dictionary.csv` | Column definitions for the master table |
| `docs/paper_to_files.md` | Mapping from every paper table/figure to the exact file in `results/` |
| `data/README.md` | How to obtain RecGym |

---

## Run order

The four notebooks must be run in order; each reads the previous stage's output.

| Stage | Notebook | Reads | Writes |
|---|---|---|---|
| 00 | `notebooks/00_data_audit.ipynb` | `RecGym.csv` (UCI) | `protocol/*.json`, `protocol/windows_index.parquet`, audit report and audit tables |
| 01 | `notebooks/01_classical_models.ipynb` | `RecGym.csv`, `protocol/windows_index.parquet` | `results/raw/classical_full/` (RF, SVM, XGB) |
| 02 | `notebooks/02_cnn.ipynb` | `RecGym.csv`, `protocol/windows_index.parquet`, `results/raw/classical_full/` | `results/raw/cnn_full/` (CNN) |
| 03 | `notebooks/03_analysis.ipynb` | `results/raw/classical_full/`, `results/raw/cnn_full/` | `results/tables/`, `results/figures/`, `results/analysis_checks/` |

Notebook 03 trains nothing. Every reported number is recomputed from the saved `results.csv` and `confusion_long.csv` files.

### Configuration

All four notebooks are configured through environment variables with relative defaults, so they run from the repository root without edits:

| Variable | Default | Used by |
|---|---|---|
| `RECGYM_CSV` | `data/RecGym.csv` | 00, 01, 02 |
| `RESULTS_DIR` | `results/raw/data_audit` (00), `results/raw/classical` (01), `results/raw/cnn` (02), `results/analysis` (03) | 00, 01, 02, 03 |
| `INPUT_DIR` | `results/raw` | 03 |
| `CLASSICAL_DIR` | `results/raw/classical` | 02 |
| `SMOKE_TEST` | `1` (a small check run) | 01, 02 |
| `RECGYM_SKIP_HASH` | unset (the SHA-256 of the input CSV is enforced) | 01, 02 |

To run the real grid instead of the smoke test:

```bash
export SMOKE_TEST=0
```

Notebook 02 requires a GPU for the full grid (it raises by default on CPU unless `ALLOW_CPU = True` is set).

---

## Reproducing the results

```bash
git clone https://github.com/darkEye-2021831014/AxisFit.git
cd AxisFit
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. get the data (see data/README.md)
mkdir -p data
# place RecGym.csv at data/RecGym.csv, or let notebook 00 fetch it from UCI

# 2. run the notebooks in order
jupyter nbconvert --to notebook --execute --inplace notebooks/00_data_audit.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/01_classical_models.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_cnn.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_analysis.ipynb
```

The full grid is 1,800 evaluation units (3 positions × 15 configurations × 10 LOSO folds × 4 models) and takes a substantial amount of compute, especially for the CNN. `SMOKE_TEST=1` (the default) runs a reduced grid for a quick sanity check.

### Protocol (fixed before any test was run)

- 15 axis configurations; no configuration mixes accelerometer and gyroscope axes, so each reduction removes a channel from one sensor.
- 4 s windows (80 samples) at 20 Hz with 50 % overlap, never crossing a run boundary (0.859 % of rows excluded).
- Leave-one-subject-out cross-validation, 10 folds; normalisation statistics and class weights come from the nine training subjects only.
- Primary metric: macro-F1 over all 12 labels including `Null`. Sensitivity analysis repeats everything with `Null` excluded.
- Two-sided Wilcoxon signed-rank tests on 10 paired subject-level values, with Holm correction within pre-declared families, plus percentile bootstrap 95 % CIs (10,000 resamples).
- Seed 42 throughout; no hyperparameter tuning and no early stopping.

---

## What is included and what is not

**Included:** all four notebooks (outputs stripped), the protocol manifests, the raw per-fold results of both model stages, the analysis integrity checks, all 31 tables and all 13 figures as PNG.

**Not included:**

- **The RecGym dataset itself.** It is redistributed by the UCI Machine Learning Repository under CC BY 4.0 and is fetched by notebook 00 (see `data/README.md`). Its SHA-256 is asserted in every notebook.
- **Large per-cell confusion matrices** (`confusion_long.csv` for the classical and CNN stages, and the pooled confusion table). These are too large for Git; they are attached to the Zenodo release instead — see `docs/paper_to_files.md`.
- **Model checkpoints and the smoke-test archives.** Neither is needed to recompute the reported numbers.
- **The manuscript source, cover letter and reviewer responses.** These are private working material and are not part of this public repository.

Everything reported in the paper can be recomputed from the files in `results/` using notebook 03, or inspected directly from the CSVs.

---

## Data and code availability

RecGym is available from the UCI Machine Learning Repository (UCI id 1128, DOI [10.24432/C5PW4K](https://doi.org/10.24432/C5PW4K), CC BY 4.0). The analysis code, protocol manifests and per-cell results are available at <https://github.com/darkEye-2021831014/AxisFit> and will be archived with a versioned DOI on Zenodo: **[Zenodo DOI to be inserted after release]**.

---

## Citation

If you use this work, please cite the paper. A `CITATION.cff` file is included; the versioned Zenodo DOI will be added once the archive record is published.

> A. Islam, *"Placement-Specific Axis Reduction of Wearable Inertial Sensors for Gym Exercise Recognition,"* IEEE Sensors Journal, under review.

---

## License

Code in this repository is released under the MIT License (see `LICENSE`). The RecGym dataset is *not* redistributed here and remains under CC BY 4.0 from the UCI Machine Learning Repository.
