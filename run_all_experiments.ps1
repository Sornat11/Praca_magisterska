# Skrypt do seryjnego uruchamiania eksperymentów (PowerShell)
# Uruchomienie: .\run_all_experiments.ps1

$PythonPath = ".\venv\Scripts\python.exe"

Write-Host "=== Rozpoczynam nocna serie eksperymentow ===" -ForegroundColor Cyan

# 1. BPR-MF
Write-Host "[1/4] Uruchamiam BPR-MF (Baseline)..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_experiment.py --model BPR --dataset ml-100k --config 2_Experiments/Configs/bpr.yaml

# 2. NeuMF (NCF)
Write-Host "[2/4] Uruchamiam NeuMF (Deep Learning)..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_experiment.py --model NeuMF --dataset ml-100k --config 2_Experiments/Configs/ncf.yaml

# 3. LightGCN (GNN)
Write-Host "[3/4] Uruchamiam LightGCN (Graph Neural Network)..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_experiment.py --model LightGCN --dataset ml-100k --config 2_Experiments/Configs/gnn.yaml

# 4. ItemKNN
Write-Host "[4/4] Uruchamiam ItemKNN..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_experiment.py --model ItemKNN --dataset ml-100k --config 2_Experiments/Configs/itemknn.yaml

Write-Host "=== Wszystkie eksperymenty zakonczone! ===" -ForegroundColor Green

# 5. Agregacja wynikow do Excela/CSV
Write-Host "Aktualizuje zbiorcza tabele wynikow..." -ForegroundColor Cyan
& $PythonPath 3_Evaluation/aggregate_results.py

Write-Host "Gotowe! Wyniki znajdziesz w folderze 'log/' oraz w '3_Evaluation/experiment_summary.csv'."
