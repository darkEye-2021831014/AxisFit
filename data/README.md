# Data

## The RecGym dataset

| | |
|---|---|
| **Name** | RecGym — Gym Workouts Recognition Dataset with IMU and Capacitive Sensor |
| **UCI id** | [1128](https://archive.ics.uci.edu/dataset/1128/recgym+gym+workouts+recognition+dataset+with+imu+and+capacitive+sensor) |
| **DOI** | [10.24432/C5PW4K](https://doi.org/10.24432/C5PW4K) |
| **Licence** | CC BY 4.0 |
| **Contents** | 10 volunteers × 5 sessions × 3 body positions (wrist, pocket, leg/calf); 11 gym workouts plus a `Null` class; 12 classes in total; 4,703,320 rows; six inertial channels (`A_x`, `A_y`, `A_z`, `G_x`, `G_y`, `G_z`) plus a capacitive channel `C_1`; nominal sampling rate 20 Hz |

**The raw data are not redistributed in this repository.** Please obtain them from the UCI Machine Learning Repository under the CC BY 4.0 licence and place the file at `data/RecGym.csv`.

## Obtaining the file

### Option A — download it manually (recommended)

1. Open the UCI dataset page: <https://archive.ics.uci.edu/dataset/1128/recgym+gym+workouts+recognition+dataset+with+imu+and+capacitive+sensor>
2. Download the dataset archive and extract it.
3. Copy the RecGym CSV to `data/RecGym.csv`:

```bash
mkdir -p data
cp /path/to/RecGym.csv data/RecGym.csv
```

### Option B — let notebook 00 fetch it

Notebook `00_data_audit.ipynb` resolves the input file in this order:

1. the path in the `RECGYM_CSV` environment variable (default `data/RecGym.csv`);
2. a RecGym CSV already present in the working directory or in the cache directory;
3. a direct download of the UCI archive;
4. `ucimlrepo` (`fetch_ucirepo(id=1128)`), which is installed on demand.

On Colab it additionally offers a manual file upload. On Kaggle it also looks in `/kaggle/input`.

## Integrity check

Every notebook asserts the SHA-256 of the input file:

```
2031c077a57e93d6b5c39da198470cb6c9b1a3c0652ab57cfc5d6a39bfa840e9
```

You can verify it yourself:

```bash
shasum -a 256 data/RecGym.csv     # macOS
sha256sum data/RecGym.csv         # Linux
```

Set `RECGYM_SKIP_HASH=1` to bypass the check (not recommended). The hash is recorded in `results/raw/classical_full/environment.json` and `results/raw/cnn_full/environment.json`.

## What this repository does *not* contain

- The RecGym CSV itself (CC BY 4.0, redistributed by UCI — not by this repository).
- `recgym_canonical.parquet` (a compact copy of the raw data) and `cli_test_sample.csv.gz` (a small CLI test sample), both produced by notebook 00 and excluded on size grounds.
- The large per-cell confusion matrices (`confusion_long.csv`). See [`docs/paper_to_files.md`](../docs/paper_to_files.md) for where they are attached instead.

## Note on the capacitive channel

The dataset also contains a capacitive channel `C_1`. It was **excluded** from this study: the work concerns axis-level reduction of the six inertial channels only. The `COL_CHANNELS` override in notebook 00 still maps it, so it can be included by editing that config cell.
