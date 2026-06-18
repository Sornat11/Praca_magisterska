# Skrypt do seryjnego uruchamiania eksperymentów (PowerShell)
# Uruchomienie: .\run_all_experiments.ps1

$PythonPath = ".\venv\Scripts\python.exe"

Write-Host "=== Rozpoczynam nocna serie eksperymentow ===" -ForegroundColor Cyan

# 1. BPR-MF
Write-Host "[1/3] Uruchamiam BPR-MF (Baseline)..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_bpr.py

# 2. NeuMF (NCF)
Write-Host "[2/3] Uruchamiam NeuMF (Deep Learning)..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_ncf.py

# 3. LightGCN (GNN)
Write-Host "[3/3] Uruchamiam LightGCN (Graph Neural Network)..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_gnn.py

Write-Host "=== Wszystkie eksperymenty zakonczone! ===" -ForegroundColor Green

# 4. Agregacja wynikow do Excela/CSV
Write-Host "Aktualizuje zbiorcza tabele wynikow..." -ForegroundColor Cyan
& $PythonPath 3_Evaluation/aggregate_results.py

Write-Host "Gotowe! Wyniki znajdziesz w folderze 'log/' oraz w '3_Evaluation/experiment_summary.csv'."
