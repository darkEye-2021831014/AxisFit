# Placement-specific inertial-axis reduction for wearable gym exercise recognition

Wearable inertial sensing supports gym exercise recognition, but every accelerometer and gyroscope axis adds sampling, transmission and storage cost, and it is unclear which axes are worth keeping. This repository contains the analysis for a study that evaluated **30 axis configurations** at three body positions (wrist, pocket, calf) of the public **RecGym** dataset: the full six-axis set, drop-one subsets, same-sensor and mixed accelerometer–gyroscope pairs, pure triples and single axes. A random forest, an SVM, gradient-boosted trees and a 1-D CNN were scored by macro-F1 under leave-one-subject-out (LOSO) validation (10 subjects, 12 labels, 105,728 windows).

Main findings (details and caveats are in the paper):

* Axis reduction significantly decreased macro-F1 in **160 of 168** primary-group comparisons with the full set, and **103 of 108** mixed-pair comparisons.
* Tolerance is placement-specific: at the **calf**, the gyroscope triple retained 95.8–97.9 % of full-set macro-F1 at half the data rate; the **wrist** tolerated reduction least.
* Dropping one axis was usually cheap (64 of 72 drop-one tests above the −0.05 margin); replacing two axes with a mixed pair usually was not (1 of 108).
* The accelerometer-versus-gyroscope balance changed with placement. Mixed pairs beat the mean pure pair in 8 of 12 position–model cells but not reliably the best pure pair.
* Axis reduction cuts data rate exactly, but not reliably CPU time or model size. Power consumption was **not** measured.

This is the reproducibility repository for the paper *"Placement-specific inertial-axis reduction for wearable gym exercise recognition"*, submitted to *Pervasive and Mobile Computing* (Elsevier).

---

## The 30-configuration lattice

The lattice has three groups and is **deliberately incomplete**; the paper makes no claim about configurations that were not run.

| Group | Configurations | Count | Channels | Seeds |
|---|---|---|---|---|
| **Primary** | six-axis set; two pure triples (`acc-3`, `gyro-3`); three accelerometer pairs; three gyroscope pairs; six single axes | 15 | 6, 3, 2, 1 | 42–44 (classical), 42–46 (CNN) |
| **Drop-one** | six-axis set with one axis removed | 6 | 5 | 42 |
| **Mixed-pair** | one accelerometer axis with one gyroscope axis | 9 | 2 | 42 |

Not run: mixed three-axis subsets (the three-axis group is the two pure triples only) and all four-axis subsets (the five-axis group is drop-one only). Definitions: `protocol/axis_configs.json` (primary 15) and `protocol/axis_configs_extended.json` (all 30).

---

## Repository layout

| Path | Contents |
|---|---|
| `notebooks/` | All analysis notebooks, outputs stripped: base `00` → `03` (primary group, seed 42) and extended `04b`, `02_cnn_seeds43-46`, `04c`, `05`, `06` (extra seeds, latency/cost, drop-one and mixed-pair analysis) |
| `protocol/` | JSON/parquet manifests that fix the protocol: axis configurations, LOSO folds, label and position maps, subject list, audit summary, compute plan, window metadata and index |
| `results/raw/` | Raw per-fold output: base runs (`classical_full/`, `cnn_full/`) and extended runs (`extended_full/`, `classical_seed43/`, `classical_seed44/`, `cnn_seeds43-46_full/`, `latency_full/`) |
| `results/tables/` | Base-analysis tables as CSV, indexed by `TABLES_INDEX.csv` |
| `results/tables_extended/` | Extended-analysis tables (drop-one, mixed-pair, seeds, systems cost) as CSV |
| `results/tables_seeds/` | Seed-variability tables from notebook 04c |
| `results/figures/` | `Fig01`, `Fig02` (paper schematics, PDF + PNG) and the base-analysis figures `F1`–`F9` |
| `results/figures_extended/` | `FX1`–`FX11`, the paper's result figures (PDF + PNG) |
| `results/analysis_checks/` | Integrity checks, analysis manifest, latency note and run log of notebook 03; `extended/` holds the checks of notebook 06 |
| `results/master_results.csv` | Long-format master table of the base results, with a column dictionary |
| `docs/paper_to_files.md` | Mapping from every paper table and figure to the file that holds it |
| `scripts/verify_paper_claims.py` | Recomputes the primary-group numbers quoted in the paper from the files here |
| `scripts/check_release.py` | Pre-push completeness and notebook-validity check |
| `data/README.md` | How to obtain RecGym |

---

## Run order

The base notebooks must be run in order; each reads the previous stage's output.

| Stage | Notebook | Reads | Writes |
|---|---|---|---|
| 00 | `notebooks/00_data_audit.ipynb` | `RecGym.csv` (UCI) | `protocol/*`, audit report and tables |
| 01 | `notebooks/01_classical_models.ipynb` | `RecGym.csv`, `protocol/windows_index.parquet` | `results/raw/classical_full/` (RF, SVM, XGB) |
| 02 | `notebooks/02_cnn.ipynb` | `RecGym.csv`, `protocol/windows_index.parquet`, `results/raw/classical_full/` | `results/raw/cnn_full/` (CNN) |
| 03 | `notebooks/03_analysis.ipynb` | `results/raw/classical_full/`, `results/raw/cnn_full/` | `results/tables/`, `results/figures/`, `results/analysis_checks/` |

The extension notebooks then run against the same protocol manifests:

| Stage | Notebook | Reads | Writes |
|---|---|---|---|
| 04b | `notebooks/04b_classical_seeds.ipynb` | `protocol/windows_index.parquet` | `results/raw/classical_seed43/`, `results/raw/classical_seed44/` |
| 02-seeds | `notebooks/02_cnn_seeds43-46.ipynb` | `protocol/windows_index.parquet` | `results/raw/cnn_seeds43-46_full/` |
| 04c | `notebooks/04c_seed_analysis.ipynb` | the seed runs | `results/tables_seeds/` |
| 05 | `notebooks/05_latency_and_cost.ipynb` | the per-fold results | `results/raw/latency_full/` |
| 06 | `notebooks/06_analysis_extended.ipynb` | per-fold results plus the extension runs | `results/tables_extended/`, `results/analysis_checks/extended/` |

Notebooks 03, 04c and 06 train nothing: every reported number is recomputed from the saved `results.csv` and `confusion_long.csv` files.

### Configuration

The base notebooks are configured through environment variables with relative defaults, so they run from the repository root without edits:

| Variable | Default | Used by |
|---|---|---|
| `RECGYM_CSV` | `data/RecGym.csv` | 00, 01, 02 |
| `RESULTS_DIR` | `results/raw/data_audit` (00), `results/raw/classical` (01), `results/raw/cnn` (02), `results/analysis` (03) | 00, 01, 02, 03 |
| `INPUT_DIR` | `results/raw` | 03 |
| `CLASSICAL_DIR` | `results/raw/classical` | 02 |
| `SMOKE_TEST` | `1` (a small check run) | 01, 02 |
| `RECGYM_SKIP_HASH` | unset (the SHA-256 of the input CSV is enforced) | 01, 02 |

The defaults write to separate directories (`results/raw/classical/`, `results/raw/cnn/`, `results/analysis/`), so a rerun does not overwrite the released results in `results/raw/classical_full/`, `results/raw/cnn_full/` and `results/tables/`. To run the real grid instead of the smoke test, `export SMOKE_TEST=0`. Notebook 02 requires a GPU for the full grid (it raises on CPU unless `ALLOW_CPU = True` is set).

---

## Reproducing the results

```bash
git clone https://github.com/darkEye-2021831014/AxisFit.git
cd AxisFit
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. get the data (see data/README.md)
mkdir -p data      # place RecGym.csv at data/RecGym.csv, or let notebook 00 fetch it from UCI

# 2. run the base notebooks in order
jupyter nbconvert --to notebook --execute --inplace notebooks/00_data_audit.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/01_classical_models.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_cnn.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_analysis.ipynb

# 3. check the paper's primary-group numbers against the released results (no data needed)
python scripts/verify_paper_claims.py
```

The full lattice is **3,600 evaluation cells** (3 positions × 30 configurations × 10 LOSO folds × 4 models); the 15 primary configurations account for 1,800 of them. This takes substantial compute, especially for the CNN. `SMOKE_TEST=1` (the default) runs a reduced grid for a quick sanity check.

### Protocol (fixed before any test was run)

* 30 axis configurations in three groups. The mixed-pair group combines accelerometer and gyroscope axes, so this is not a within-sensor-only study.
* 4 s windows (80 samples) at a nominal 20 Hz with 50 % overlap, never crossing a (subject, position, session, label) run boundary (0.859 % of rows excluded).
* LOSO cross-validation, 10 folds; normalisation statistics and class weights come from the nine training subjects only. A label-shuffle control gave macro-F1 of 0.0576 (RF) and 0.0871 (XGB) against a chance level of 0.0833.
* Primary metric: macro-F1 over all 12 labels including `Null`; a sensitivity analysis repeats the comparisons with `Null` excluded.
* Two-sided Wilcoxon signed-rank tests on 10 paired subject-level values with Holm correction within pre-declared families, plus percentile bootstrap 95 % CIs (10,000 resamples over subjects). A reduced configuration is called non-inferior when the lower bound of its paired bootstrap interval against six axes exceeds −0.05 macro-F1 (a descriptive margin, not application-derived).
* Seeds 42–44 (classical) and 42–46 (CNN) for the primary group; seed 42 only for the drop-one and mixed-pair groups, because of compute budget. The measured seed spread is used as a noise reference for the single-seed results.
* No hyperparameter tuning and no early stopping.
* Latency and model size were measured on one shared virtual CPU (batch size 1, one thread). They are not edge-device figures and not energy.

---

## What is included and what is not

**Included:** the base and extension notebooks (outputs stripped), the protocol manifests, the raw per-fold results of every model stage, the integrity checks, the paper's figures (`Fig01`, `Fig02`, `FX1`–`FX11`) and the result tables.

**Not included:**

* **The RecGym dataset.** It is distributed by the UCI Machine Learning Repository under CC BY 4.0 and fetched by notebook 00 (see `data/README.md`). Its SHA-256 is asserted in every notebook.
* **The per-cell confusion matrices** (`confusion_long.csv` for the classical and CNN stages and the pooled confusion table). They exceed the file-size limit of the hosting service and are available from the corresponding author on request, as stated in the paper.
* **Model checkpoints.** They are not needed to recompute the reported numbers.
* **The manuscript source, cover letter and reviewer responses.**

---

## Data and code availability

RecGym is available from the UCI Machine Learning Repository (UCI id 1128, DOI [10.24432/C5PW4K](https://doi.org/10.24432/C5PW4K), CC BY 4.0). The analysis code, protocol manifests, per-configuration results and the tables and figures reported in the paper are available at <https://github.com/darkEye-2021831014/AxisFit>.

---

## Citation

If you use this work, please cite the paper (a `CITATION.cff` file is included):

> A. Islam, *"Placement-specific inertial-axis reduction for wearable gym exercise recognition,"* *Pervasive and Mobile Computing* (Elsevier), submitted. ORCID [0009-0009-9792-0746](https://orcid.org/0009-0009-9792-0746).

---

## License

Code in this repository is released under the MIT License (see `LICENSE`). The RecGym dataset is not redistributed here and remains under CC BY 4.0 from the UCI Machine Learning Repository.
