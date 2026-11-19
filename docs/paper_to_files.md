# Paper → files map

Maps every table and figure of *"Placement-specific inertial-axis reduction for wearable gym exercise recognition"* (main text and supplementary material) to the file in this repository that holds it and the notebook that produces it.

Paths are relative to the repository root. The paper is a two-stage analysis, and the repository mirrors that:

* **Base analysis** — notebooks `00`–`03`, the 15 *primary* configurations, seed 42. Notebooks `00`–`03`.
* **Extended analysis** — drop-one and mixed-pair groups, the extra seeds, and the latency/cost measurement. Notebooks `02_cnn_seeds43-46`, `04b`, `04c`, `05`, `06`; raw results in `results/raw/`, tables in `results/tables_extended/` and `results/tables_seeds/`.

All notebooks are in `notebooks/` and all outputs in `results/`.

---

## Main-text figures

Numbered in order of appearance in the paper.

| Paper | Content | File | Produced by |
|---|---|---|---|
| Fig. 1 | Analysis pipeline | `results/figures/Fig01_pipeline.pdf` (+ `.png`) | hand-made schematic, no script |
| Fig. 2 | Sensor positions | `results/figures/Fig02_sensor_positions.pdf` (+ `.png`) | hand-made schematic, no script |
| Fig. 3 | Mean macro-F1, 30 configurations × 3 positions × 4 models | `results/figures_extended/FX1_macroF1_heatmap_30_configs.pdf` | `notebooks/06_analysis_extended.ipynb` |
| Fig. 4 | Best, median and worst retained macro-F1 by axis count | `results/figures_extended/FX3_best_median_worst_by_channel_count.pdf` | 06 |
| Fig. 5 | Mixed vs pure pairs (complementarity) | `results/figures_extended/FX9_complementarity_mixed_vs_pure.pdf` | 06 |
| Fig. 6 | Pair configurations grouped by type | `results/figures_extended/FX5_pairs_by_type.pdf` | 06 |
| Fig. 7 | Per-class F1 change, mix-AxGz vs six axes | `results/figures_extended/FX10_perclass_mixAxGz.pdf` | 06 |
| Fig. 8 | Selection optimism | `results/figures_extended/FX11_selection_optimism.pdf` | 06 |
| Fig. 9 | Single-window CPU latency and model size vs axis count | `results/figures_extended/FX8_systems_vs_channels.pdf` | `notebooks/05_latency_and_cost.ipynb` |
| Fig. 10 | Accuracy–data-rate Pareto fronts | `results/figures_extended/FX4_pareto_f1_vs_data_rate.pdf` | 05 |

Every `FX*` figure is provided as PDF (the version used in the paper) and as a PNG rendering of that PDF.

## Main-text table

| Paper | Content | Source |
|---|---|---|
| Table 1 | Best configuration per reduced axis count and retained macro-F1 (%) | Extended analysis (`notebooks/06_analysis_extended.ipynb`). The **3-axis and 1-axis columns** and the six-axis baselines come from the primary group and are recomputed from `results/master_results.csv` by `scripts/verify_paper_claims.py`. The 5-axis (drop-one) and 2-axis (mixed-pair) columns need the extended results. |

---

## Supplementary material

| Supp. | Content | Source |
|---|---|---|
| S2 | The 30 configurations by group and axis count | `protocol/axis_configs.json` (primary 15) and `protocol/axis_configs_extended.json` (all 30) |
| S3 | Primary group: 14 reduced configurations vs six axes, per position | `results/tables/Table09_long.csv` — the same 168 comparisons (160 Holm-significant decreases; the Calf/RF rows spot-checked against the supplement agree) |
| S4, S5 | Drop-one and mixed-pair groups vs six axes | extended analysis (06) |
| S6, S7 | Best/median/worst by axis count; practical guidance | extended analysis (06) |
| S8 | Mixed vs pure pairs, three contrasts | extended analysis (06) |
| S9 | Marginal gain of each axis | primary-group version: `results/tables/Table06_axis_marginal_gain.csv` (model-averaged values quoted in the text are recomputed by `scripts/verify_paper_claims.py`); the supplement's version is from 06 |
| S10 | Agreement between model families (Kendall's W) | extended analysis (06) |
| S11 | Seed variability | `notebooks/04c_seed_analysis.ipynb` → `results/tables_seeds/` |
| S12, S13 | Systems cost by axis count; data volume | `notebooks/05_latency_and_cost.ipynb` → `results/raw/latency_full/` |
| S14 | Per-class changes, mix-AxGz | extended analysis (06) |
| S15, S16 | Selection optimism; margin map by seed | extended analysis (06) |
| S17 | Integrity checks and controls (anchor check, label-shuffle, Null concordance) | extended analysis (06). Base-run counterparts: `results/analysis_checks/checks/`, `results/raw/cnn_full/sanity_checks.json`, `results/tables/TableS5b_null_concordance.csv` |
| S18 | Figures not in the main text | `results/figures_extended/FX2_E1_E2_vs_6axis.pdf`, `FX6_model_ranking_agreement.pdf`, `FX7_seed_sd_by_channels.pdf` |

---

## What is checked automatically

`python scripts/verify_paper_claims.py` recomputes, from files in this repository only:

* the twelve six-axis macro-F1 values (0.886, 0.850, 0.935, 0.932 wrist; 0.797, 0.786, 0.854, 0.812 calf; 0.547, 0.595, 0.687, 0.653 pocket);
* the 3-axis and 1-axis columns of Table 1 (best configuration and retained %), 12 rows;
* 160 of 168 Holm-significant decreases in the primary group;
* the model-averaged marginal gains quoted under RQ3.

Claims about the drop-one group (28 of 72; 64 of 72 above the −0.05 bound), the mixed-pair group (103 of 108), seeds, the Pareto front and latency need the extended results and are not checked by this script.

---

## Base-analysis outputs that are not printed in the paper

`results/figures/F1…F9` and `results/tables/*` are the outputs of notebook 03 for the 15-configuration base analysis (seed 42). They were produced before the lattice was extended and are kept as the base record; the paper's figures above supersede them. `results/tables/TABLES_INDEX.csv` indexes them.

| Group | Path |
|---|---|
| Master long-format results (15 configs) | `results/master_results.csv`, `results/master_results_dictionary.csv` |
| Per-fold results | `results/raw/classical_full/results.csv`, `results/raw/cnn_full/results.csv` |
| Run configuration, environment, logs | `results/raw/*/run_config.json`, `environment.json`, `run_log.txt` |
| CNN label-shuffle control | `results/raw/cnn_full/sanity_checks.json` |
| Integrity checks, manifest, latency note | `results/analysis_checks/` |
| Protocol manifests | `protocol/` |

## Not stored in Git

The per-cell confusion matrices (`confusion_long.csv` for the classical and CNN stages, and the pooled confusion table) exceed what is practical to host here. As stated in the paper's Data availability section, they are available from the corresponding author on request. Notebook 03 reads the two `confusion_long.csv` files to build the per-class and confusion outputs, so those outputs cannot be regenerated without them; all other tables can.
