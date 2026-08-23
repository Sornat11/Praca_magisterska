# Skrypt do seryjnego uruchamiania optymalizacji hiperparametrów (PowerShell)
# Uruchomienie: .\run_all_hyper.ps1

$PythonPath = ".\venv\Scripts\python.exe"

Write-Host "=== Rozpoczynam serie optymalizacji hiperparametrow ===" -ForegroundColor Cyan

# 1. BPR-MF
Write-Host "[1/4] Uruchamiam optymalizacje BPR-MF..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_hyper.py --model BPR --config 2_Experiments/Configs/bpr.yaml --hyper 2_Experiments/Hyperparams/bpr.hyper --algo exhaustive

# 2. NeuMF (NCF)
Write-Host "[2/4] Uruchamiam optymalizacje NeuMF (NCF)..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_hyper.py --model NeuMF --config 2_Experiments/Configs/ncf.yaml --hyper 2_Experiments/Hyperparams/ncf.hyper --algo exhaustive

# 3. LightGCN (GNN)
Write-Host "[3/4] Uruchamiam optymalizacje LightGCN (GNN)..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_hyper.py --model LightGCN --config 2_Experiments/Configs/gnn.yaml --hyper 2_Experiments/Hyperparams/gnn.hyper --algo exhaustive

# 4. ItemKNN
Write-Host "[4/4] Uruchamiam optymalizacje ItemKNN..." -ForegroundColor Yellow
& $PythonPath 2_Experiments/run_hyper.py --model ItemKNN --config 2_Experiments/Configs/itemknn.yaml --hyper 2_Experiments/Hyperparams/itemknn.hyper --algo exhaustive

Write-Host "=== Wszystkie optymalizacje zakonczone! ===" -ForegroundColor Green
Write-Host "Wyniki znajdziesz w folderze '3_Evaluation/Reports/'."
