#!/bin/bash
# Skrypt do seryjnego uruchamiania optymalizacji hiperparametrów na systemie Linux (np. Azure VM)
# Uruchomienie: chmod +x run_all_hyper.sh && ./run_all_hyper.sh

PYTHON_PATH="./venv/bin/python"

echo -e "\e[36m=== Rozpoczynam serie optymalizacji hiperparametrow na Azure (GPU/CPU) ===\e[0m"

# 1. BPR-MF
echo -e "\e[33m[1/3] Uruchamiam optymalizacje BPR-MF...\e[0m"
$PYTHON_PATH 2_Experiments/run_hyper_bpr.py

# 2. NeuMF (NCF)
echo -e "\e[33m[2/3] Uruchamiam optymalizacje NeuMF (NCF)...\e[0m"
$PYTHON_PATH 2_Experiments/run_hyper_ncf.py

# 3. LightGCN (GNN)
echo -e "\e[33m[3/3] Uruchamiam optymalizacje LightGCN (GNN)...\e[0m"
$PYTHON_PATH 2_Experiments/run_hyper_gnn.py

echo -e "\e[32m=== Wszystkie optymalizacje zakonczone! ===\e[0m"
echo "Wyniki znajdziesz w folderze '3_Evaluation/Reports/'."
