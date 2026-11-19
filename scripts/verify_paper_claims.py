#!/usr/bin/env python3
"""Recompute, from files in this repository, the paper numbers that depend only
on the primary group (15 configurations, seed 42).

Checked here (paper: "Placement-specific inertial-axis reduction for wearable
gym exercise recognition"):
  * the twelve six-axis macro-F1 values (Results, "Full six-axis performance")
  * the 3-axis and 1-axis columns of Table 1 (best configuration and retained %)
  * 160 of 168 Holm-significant decreases in the primary group
  * the model-averaged marginal gains quoted in the text (RQ3)

Claims that need the extended lattice (drop-one, mixed-pair, seeds, latency)
cannot be checked from this folder alone; see docs/paper_to_files.md.

Run from the repository root:  python scripts/verify_paper_claims.py
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
res = pd.read_csv(ROOT / "results" / "master_results.csv")
fails = []


def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (f"  {detail}" if detail and not ok else ""))
    if not ok:
        fails.append(name)


# --- six-axis macro-F1 (text) -------------------------------------------------
SIX = {("wrist", "RF"): .886, ("wrist", "SVM"): .850, ("wrist", "XGB"): .935, ("wrist", "CNN"): .932,
       ("leg", "RF"): .797, ("leg", "SVM"): .786, ("leg", "XGB"): .854, ("leg", "CNN"): .812,
       ("pocket", "RF"): .547, ("pocket", "SVM"): .595, ("pocket", "XGB"): .687, ("pocket", "CNN"): .653}
bad = [(p, m) for (p, m), v in SIX.items()
       if abs(round(res[(res.placement == p) & (res.model == m) & (res.axis_config == "6-axis")]
                    .macro_f1_mean.iloc[0], 3) - v) > 6e-4]
check("six-axis macro-F1, 12 cells", not bad, str(bad))

# --- Table 1: 3-axis and 1-axis columns --------------------------------------
T1 = {("leg", "RF"): ("gyro-3", 97.1, "single-Gz", 90.6), ("leg", "SVM"): ("gyro-3", 95.8, "single-Gz", 86.3),
      ("leg", "XGB"): ("gyro-3", 96.2, "single-Gz", 86.9), ("leg", "CNN"): ("gyro-3", 97.9, "single-Gz", 91.1),
      ("pocket", "RF"): ("acc-3", 95.4, "single-Ax", 85.5), ("pocket", "SVM"): ("acc-3", 92.5, "single-Ax", 75.7),
      ("pocket", "XGB"): ("acc-3", 92.4, "single-Ax", 75.2), ("pocket", "CNN"): ("acc-3", 94.8, "single-Ax", 79.2),
      ("wrist", "RF"): ("acc-3", 88.9, "single-Gz", 70.2), ("wrist", "SVM"): ("acc-3", 88.3, "single-Gz", 70.5),
      ("wrist", "XGB"): ("acc-3", 91.8, "single-Gz", 71.1), ("wrist", "CNN"): ("acc-3", 93.8, "single-Gz", 75.9)}
singles = [f"single-{a}" for a in ("Ax", "Ay", "Az", "Gx", "Gy", "Gz")]
bad = []
for (p, m), (c3, r3, c1, r1) in T1.items():
    d = res[(res.placement == p) & (res.model == m)].set_index("axis_config").macro_f1_mean
    t3, t1 = d[["acc-3", "gyro-3"]], d[singles]
    if (t3.idxmax(), t1.idxmax()) != (c3, c1) or abs(100 * t3.max() / d["6-axis"] - r3) > .06 \
            or abs(100 * t1.max() / d["6-axis"] - r1) > .06:
        bad.append((p, m))
check("Table 1, 3-axis and 1-axis columns, 12 rows", not bad, str(bad))

# --- 160 / 168 ----------------------------------------------------------------
t9 = pd.read_csv(ROOT / "results" / "tables" / "Table09_long.csv")
check("primary group: 168 comparisons", len(t9) == 168)
check("primary group: 160 Holm-significant decreases",
      int(((t9.p_holm_family < .05) & (t9.mean_diff < 0)).sum()) == 160)

# --- marginal gains (model-averaged) -----------------------------------------
mg = pd.read_csv(ROOT / "results" / "tables" / "Table06_axis_marginal_gain.csv")
for c in ("Ax", "Ay", "Az", "Gx", "Gy", "Gz"):
    mg[c] = mg[c].str.extract(r"([+-]?\d*\.\d+)")[0].astype(float)
avg = mg.groupby("position")[["Ax", "Gz"]].mean().round(3)
QUOTED = {("wrist", "Ax"): .173, ("wrist", "Gz"): .170, ("leg", "Gz"): .210,
          ("leg", "Ax"): .109, ("pocket", "Ax"): .102, ("pocket", "Gz"): .086}
bad = [(k, avg.loc[k[0], k[1]], v) for k, v in QUOTED.items() if abs(avg.loc[k[0], k[1]] - v) > .0015]
check("marginal gains quoted in RQ3, 6 values (tolerance 0.0015)", not bad, str(bad))

print("\n%d check(s) failed" % len(fails) if fails else "\nAll checks passed")
sys.exit(1 if fails else 0)
