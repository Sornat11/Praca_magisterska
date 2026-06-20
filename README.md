# Recommender Systems Comparison - Master's Thesis

This repository contains the source code and experiments for a Master's thesis comparing Collaborative Filtering, Deep Learning, and Graph Neural Networks using a VOD service example.

## Project Structure

The project is organized into process-oriented stages:

- `0_Raw_Data/` - Original MovieLens CSV datasets (ignored by Git).
- `1_Preprocessing/` - Data analysis (EDA) and scripts to convert CSVs to RecBole format.
- `2_Experiments/` - Model configurations and execution scripts:
  - `Configs/` - YAML files with model hyperparameters (BPR, NCF, GNN).
- `3_Evaluation/` - Final results and analysis:
  - `Logs/` - Detailed training logs for each run (ignored by Git).
  - `Saved/` - Trained model weights (.pth files, ignored by Git).
  - `Reports/` - Generated tables, charts, hyperparameter summaries (`hyperparameter_summary.md`), and parsed results (`.csv` and `.result` files).
- `Datasets/` - Processed datasets in RecBole `.inter` format (ignored by Git).
- `Materials/` - Scientific literature, articles, and lecture notes.
- `Notebooks/` - Jupyter Notebooks for interactive data exploration.
- `venv/` - Python 3.12 virtual environment.

## Installation & Setup

1. **Create the environment:**
   ```bash
   py -3.12 -m venv venv
   ```

2. **Activate the environment:**
   - **PowerShell:** `.\venv\Scripts\Activate.ps1`
   - **CMD:** `.\venv\Scripts\activate.bat`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Workflow

### 1. Data Preparation
Download the raw data and convert it to the internal format:
```bash
python 1_Preprocessing/import_raw_data.py
python 1_Preprocessing/convert_to_recbole.py
```

### 2. Running Experiments
Execute specific models using the provided scripts:
- **Matrix Factorization (Baseline):**
  ```bash
  python 2_Experiments/run_bpr.py
  ```
- **Neural Collaborative Filtering (Deep Learning):**
  ```bash
  python 2_Experiments/run_ncf.py
  ```
- **LightGCN (Graph Neural Networks):**
  ```bash
  python 2_Experiments/run_gnn.py
  ```

### 3. Hyperparameter Optimization (HPO)
To find the best hyperparameters for each model using RecBole's `HyperTuning`:

- **BPR Optimization:**
  ```bash
  python 2_Experiments/run_hyper_bpr.py
  ```
- **NCF Optimization:**
  ```bash
  python 2_Experiments/run_hyper_ncf.py
  ```
- **LightGCN Optimization:**
  ```bash
  python 2_Experiments/run_hyper_gnn.py
  ```

- **Run all tuning scripts sequentially (PowerShell):**
  ```powershell
  .\run_all_hyper.ps1
  ```

Results will be saved in `3_Evaluation/Reports/` as `.result` files.

Parsed results and a comprehensive summary of the best configurations can be found in:
- `3_Evaluation/Reports/hyperparameter_summary.md` (detailed markdown report)
- `3_Evaluation/Reports/hyper_results_bpr_parsed.csv` (parsed CSV table for BPR-MF)
- `3_Evaluation/Reports/hyper_results_ncf_parsed.csv` (parsed CSV table for NCF/NeuMF)

*Note on GNN (LightGCN) tuning:* Due to the high computational cost of running GNNs (~22.4 hours per single training run on CPU), a full grid search was bypassed. Instead, we use an optimized expert configuration defined in `2_Experiments/Configs/gnn.yaml`.

## Compatibility Note (Patch)
Due to changes in `SciPy 1.11+`, the LightGCN model in RecBole requires a manual patch in the source code. If you recreate the `venv`, apply the patch using:
```bash
python -c "path='venv/Lib/site-packages/recbole/model/general_recommender/lightgcn.py'; content=open(path).read().replace('A._update(data_dict)', 'for k, v in data_dict.items(): A[k] = v'); open(path, 'w').write(content)"
```

## Author
Jakub Sornat  
Major: Computer Science and Econometrics
