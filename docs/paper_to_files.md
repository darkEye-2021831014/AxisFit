# Paper → files map

Every table and figure in *"Placement-Specific Axis Reduction of Wearable Inertial Sensors for Gym Exercise Recognition"*, mapped to the exact file in this repository and the notebook that produces it.

**Important:** the paper's numbering (Table I–IV, Fig. 1–6) does **not** correspond to the file names (`Table01…TableS8`, `F1…F9`, `Fig01`, `Fig02`). The mapping below was established by reading the LaTeX source and matching captions and cell values against the CSV and PNG files.

Paths are relative to the repository root.

---

## Paper tables

| Paper | Caption (abbreviated) | File in this repo | Produced by | Confidence |
|---|---|---|---|---|
| **Table I** | Axis Configurations Evaluated | `results/tables/Table02_axis_configurations.csv` | 00 (definition) + 03 | **High** — 15 rows matching the paper's Full/Triples/Pairs/Singles groups, with matching channel lists, data rates (120/60/40/20 Hz) and feature dimensions (90/45/30/15). |
| **Table II** | Best Reduced Configuration per Channel Count: Macro-F1 (Retained % of 6-Axis) | `results/tables/Table04_best_reduced_configs_efficiency.csv` | 03 | **High** — spot-checked against the paper: Leg RF `gyro-3` → `0.775 (97.1)`, `retained_pct=97.1`; Pocket SVM `acc-3` → `0.551 (92.5)`; Wrist CNN `single-Gz` → `0.707 (75.9)`. All match. |
| **Table III** | Accelerometer-Only Minus Gyroscope-Only Macro-F1 (acc-3 vs gyro-3); Subjects with Accelerometer Better | `results/tables/Table05a_acc_vs_gyro_gap.csv` | 03 | **High** — `level=triple` rows give exactly the paper's four models × three positions; e.g. leg/RF `-0.055 [-0.076, -0.032]`, `1/10`; pocket/CNN `+0.082`, `10/10`. Matches. |
| **Table IV** | Change in Per-Class F1 Versus 6-Axis, Gradient-Boosted Trees | `results/tables/Table08_perclass_robustness_XGB.csv` | 03 | **High** — column layout is `leg: F1 6-axis / leg: Δ acc-3 / leg: Δ gyro-3` etc., exactly the paper's layout. Spot-checked: Adductor wrist gyro-3 `-0.273*`, LegCurl wrist gyro-3 `-0.311*`, Squat leg gyro-3 `-0.078*`. Matches. |

**Supporting table for Table III.** The paper states the gap is reported at three levels (triple, pair, single) in the text and in the figure caption of Fig. 4. The triples are in `Table05a_acc_vs_gyro_gap.csv`; the between-position difference (calf vs pocket) quoted in the text ("−0.111 to −0.133") is in `results/tables/Table05b_gap_difference_between_positions.csv`. *This Table 05b is not printed in the paper — it is the source of a sentence in the Results.*

**CNN counterpart to Table IV.** `results/tables/Table08_perclass_robustness_CNN.csv` has the same layout for the CNN (the paper cites "19 of 72 changes Holm-significant, against 21 of 72 for XGB" in the text).

---

## Paper figures

| Paper | Caption (abbreviated) | File in this repo | Produced by | Confidence |
|---|---|---|---|---|
| **Fig. 1** | Overview of the analysis pipeline | `results/figures/Fig01_pipeline.png` | **Not produced by any notebook** (author's schematic) | **Medium** — the file is the exact `\includegraphics` target named in `paper.tex`, but it is a hand-made diagram, not a notebook output. See the note below. |
| **Fig. 2** | Sensor positions: wrist, pocket and calf | `results/figures/Fig02_sensor_positions.png` | **Not produced by any notebook** (author's schematic) | **Medium** — same as Fig. 1. |
| **Fig. 3** | Mean macro-F1 for all 15 axis configurations, three positions and four models | `results/figures/F1_macroF1_heatmap.png` | 03 | **High** — the `\includegraphics` target in `paper.tex` is literally `F1_macroF1_heatmap.png`. Data: `results/tables/Table03_main_LOSO_macroF1.csv`. |
| **Fig. 4** | Accelerometer-only minus gyroscope-only macro-F1, by position and subset size | `results/figures/F3_acc_minus_gyro_gap.png` | 03 | **High** — the `\includegraphics` target is `F3_acc_minus_gyro_gap.png`. Data: `results/tables/Table05a_acc_vs_gyro_gap.csv`. |
| **Fig. 5** | Marginal macro-F1 gain of each axis, by position | `results/figures/F4_axis_marginal_gain.png` | 03 | **High** — the `\includegraphics` target is `F4_axis_marginal_gain.png`. Data: `results/tables/Table06_axis_marginal_gain.csv`. |
| **Fig. 6** | Macro-F1 against retained channel count, by position and model | `results/figures/F5_performance_vs_channels.png` | 03 | **High** — the `\includegraphics` target is `F5_performance_vs_channels.png`. Data: `results/tables/Table04_best_reduced_configs_efficiency.csv` and `Table03_main_LOSO_macroF1.csv`. |

> **Note on Fig. 1 and Fig. 2.** These are the only two figures in the paper that no notebook generates. They are schematics authored by hand. Their PNGs are included here so the paper can be recompiled against this repository, but they are **not** reproducible from the released code. They are byte-identical to the copies in `Output/Figures/` and `Research/data/figures/`.

### Figures produced but not printed in the paper

These are in `results/figures/` and are available as supplementary material, but no `\includegraphics` in `paper.tex` refers to them:

| File | Content | Data source |
|---|---|---|
| `F2_reduction_vs_6axis.png` | Reduction vs 6-axis, with bootstrap CIs | `results/tables/Table09_reduction_vs_6axis_stats.csv` |
| `F6_latency_vs_f1.png` | Latency against macro-F1 | `results/tables/TableS6_efficiency_latency.csv` |
| `F7_perclass_f1_XGB.png` | Per-class F1, XGB | `results/tables/TableS3_perclass_precision_recall_f1.csv` |
| `F7_perclass_f1_CNN.png` | Per-class F1, CNN | `results/tables/TableS3_perclass_precision_recall_f1.csv` |
| `F8_confusion_XGB.png` | Confusion matrix, XGB | pooled confusion (see below) |
| `F8_confusion_CNN.png` | Confusion matrix, CNN | pooled confusion (see below) |
| `F9_per_subject.png` | Per-subject results | `results/tables/TableS7_per_subject_full.csv` |

---

## Supplementary tables

All supplementary tables live in `results/tables/`. `results/tables/TABLES_INDEX.csv` is the authoritative index: it lists, for each table, its title, row count, source file and caveats.

| File | Rows | Content |
|---|---|---|
| `Table01_dataset_protocol.csv` | 28 | Dataset and protocol summary |
| `Table03_main_LOSO_macroF1.csv` | 15 | Main LOSO macro-F1 (mean ± sd) by position × configuration × model — the source grid behind Fig. 3 |
| `Table05b_gap_difference_between_positions.csv` | 36 | Difference of the acc-minus-gyro gap between positions |
| `Table06_axis_marginal_gain.csv` | 12 | Marginal macro-F1 gain per axis — the source of Fig. 5 |
| `Table07_position_comparison.csv` | 48 | Paired position comparisons |
| `Table08_all_models_long.csv` | 288 | Per-class change vs 6-axis, all four models (long) |
| `Table09_reduction_vs_6axis_stats.csv` | 14 | Mean paired difference of each reduced configuration vs 6-axis, with bootstrap CI |
| `Table09_long.csv` | 168 | Block A full test statistics (p, dz, rank-biserial r, sign counts) |
| `Table10_per_subject_6axis.csv` | 15 | Per-subject LOSO macro-F1 for the 6-axis configuration |
| `TableS1_classical_full_results.csv` | 135 | Full classical-model results (RF, SVM, XGB) |
| `TableS2_cnn_full_results.csv` | 45 | Full CNN results (seed 42) |
| `TableS3_perclass_precision_recall_f1.csv` | 2,160 | Per-class precision, recall, F1 |
| `TableS4_top_confused_pairs.csv` | 180 | Top-5 confused exercise pairs, pooled |
| `TableS4b_top_directional_confusions.csv` | 216 | Top-6 directional confusions |
| `TableS5_null_sensitivity.csv` | 168 | Effect of excluding `Null` |
| `TableS5b_null_concordance.csv` | 3 | Concordance of primary vs Null-excluded results |
| `TableS6_efficiency_latency.csv` | 180 | Efficiency and inference latency |
| `TableS7_per_subject_full.csv` | 180 | Per-subject results for every position, model, configuration |
| `TableS8a_label_counts_rows.csv` | 12 | Rows per label and position |
| `TableS8b_rows_per_subject.csv` | 10 | Rows per subject and position |
| `TableS8c_windows_per_label.csv` | 12 | Analysed windows per label and position |
| `TableS8d_windows_per_subject.csv` | 10 | Analysed windows per subject and position |
| `TableS8e_run_lengths.csv` | 12 | Run lengths per label |
| `TableS8f_rows_lost_to_short_runs.csv` | 4 | Rows lost to runs shorter than the window |
| `TableS8g_audit_flags.csv` | 10 | Data-audit flags |

---

## Raw results and protocol manifests

| Purpose | Path |
|---|---|
| Master long-format results table | `results/master_results.csv` |
| Column dictionary for the master table | `results/master_results_dictionary.csv` |
| Per-fold results, classical (RF, SVM, XGB) | `results/raw/classical_full/results.csv` |
| Per-fold results, CNN | `results/raw/cnn_full/results.csv` |
| Classical run configuration | `results/raw/classical_full/run_config.json` |
| CNN run configuration | `results/raw/cnn_full/run_config.json` |
| Classical environment | `results/raw/classical_full/environment.json` |
| CNN environment | `results/raw/cnn_full/environment.json` |
| Classical run log | `results/raw/classical_full/run_log.txt` |
| CNN run log | `results/raw/cnn_full/run_log.txt` |
| CNN sanity checks (label-shuffle control) | `results/raw/cnn_full/sanity_checks.json` |
| CNN vs classical descriptive comparison | `results/raw/cnn_full/descriptive_vs_classical_macro_f1.csv` |
| Integrity checks | `results/analysis_checks/checks/integrity_checks.json` |
| Analysis manifest (input hashes, parameters, versions) | `results/analysis_checks/checks/analysis_manifest.json` |
| Latency measurement note | `results/analysis_checks/checks/latency_note.txt` |
| Analysis run log | `results/analysis_checks/analysis_log.txt` |
| Axis configuration definitions | `protocol/axis_configs.json` |
| LOSO fold assignment | `protocol/loso_folds.json` |
| Label map | `protocol/label_map.json` |
| Position map | `protocol/position_map.json` |
| Subject list | `protocol/subject_list.json` |
| Data-audit summary | `protocol/audit_summary.json` |
| Compute plan | `protocol/compute_plan.json` |
| Window metadata (4 s, 50 % overlap, 20 Hz) | `protocol/windows_meta.json` |
| Window index | `protocol/windows_index.parquet` |

---

## Files attached to the Zenodo release, not stored in Git

Three files are too large for Git but are needed to recompute the per-class and confusion results independently. They are attached to the Zenodo record alongside the repository:

| File | Size | Origin | Needed for |
|---|---|---|---|
| `confusion_long_classical.csv` | ~2.8 MB | `results/raw/classical_full/confusion_long.csv` | Recomputing `TableS3_perclass_precision_recall_f1.csv` and the classical confusion figure |
| `confusion_long_cnn.csv` | ~0.9 MB | `results/raw/cnn_full/confusion_long.csv` | Recomputing the CNN per-class table and `F8_confusion_CNN.png` |
| `pooled_confusion_long.csv` | ~0.5 MB | notebook 03, `tables/pooled_confusion_long.csv` | `TableS4_top_confused_pairs.csv`, `TableS4b_top_directional_confusions.csv`, `F8_confusion_*.png` |

The two `confusion_long.csv` files are also required inputs to notebook 03 (it reads them to build the per-class and confusion tables), so a run of notebook 03 needs them in place.

---

## Flagged: cannot be mapped with confidence

1. **Fig. 1 and Fig. 2** — hand-made schematics with no generating script in the repository. Included for paper recompilation, but not reproducible.
2. **`TableS4b_top_directional_confusions.csv`** — `TABLES_INDEX.csv` gives its source as `top_confusions_key_configs.csv`, a notebook-03 intermediate that is **not** included in this repository (it lives only inside the analysis archive). The supplementary table itself *is* included, so nothing is lost for reading, but it cannot be regenerated without rerunning notebook 03.
3. **PDF versions of the figures** — notebook 03 writes both `.png` and `.pdf` for each figure. Only the PNGs are included here (smaller, and the paper's `\includegraphics` targets the PNGs). The PDFs are regenerated by rerunning notebook 03.
4. **Analysis intermediate tables** — notebook 03 writes ~25 intermediate tables (e.g. `descriptive_means_by_position_model_config.csv`, `rq2_cost_table.csv`, `single_axis_ranking.csv`, `per_subject_reduction_effect_key_configs.csv`) that are the direct sources of several published tables. Only the published, renamed versions are included. `TABLES_INDEX.csv` records the source table name for each one, so the mapping is recoverable — but those exact intermediate filenames are not present under `results/tables/`.
