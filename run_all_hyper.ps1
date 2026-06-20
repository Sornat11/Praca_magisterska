# Skrypt do seryjnego uruchamiania optymalizacji hiperparametrów (PowerShell)
# Uruchomienie: .\run_all_hyper.ps1

$PythonPath = ".\venv\Scripts\python.exe"

Write-Host "=== Rozpoczynam serie optymalizacji hiperparametrow ===" -ForegroundColor Cyan

# 1. BPR-MF
Write-Host "[1/3] Uruchamiam optymalizacje BPR-MF..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_hyper_bpr.py

# 2. NeuMF (NCF)
Write-Host "[2/3] Uruchamiam optymalizacje NeuMF (NCF)..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_hyper_ncf.py

# 3. LightGCN (GNN)
Write-Host "[3/3] Uruchamiam optymalizacje LightGCN (GNN)..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_hyper_gnn.py

Write-Host "=== Wszystkie optymalizacje zakonczone! ===" -ForegroundColor Green
Write-Host "Wyniki znajdziesz w folderze '3_Evaluation/Reports/'."
