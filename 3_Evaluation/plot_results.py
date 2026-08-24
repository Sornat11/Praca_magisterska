import os
import re
import glob
import pandas as pd
import matplotlib.pyplot as plt

LOGS_DIR = 'log'
OUTPUT_IMG = 'Latex/img/learning_curves.png'
OUTPUT_SCATTER = 'Latex/img/time_vs_ndcg.png'
MODELS = ['ItemKNN', 'BPR', 'NeuMF', 'LightGCN']

def parse_best_param_log(model_name):
    # Szukaj plików .log w folderze best_param danego modelu
    search_path = os.path.join(LOGS_DIR, model_name, 'best_param', '*.log')
    log_files = glob.glob(search_path)
    
    if not log_files:
        return None
        
    # Wybierz najnowszy plik (jeśli jest ich więcej)
    latest_log = max(log_files, key=os.path.getmtime)
    
    with open(latest_log, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Krzywa uczenia (z valid_score)
    epochs = re.findall(r'epoch (\d+) evaluating.*?valid_score: ([\d\.]+)', content)
    curve = [float(score) for epoch, score in epochs]
    
    # 2. Test NDCG@10
    test_ndcg = None
    test_match = re.search(r"test result:.*?OrderedDict\(.*?\'ndcg@10\':\s*([\d\.]+)", content)
    if test_match:
        test_ndcg = float(test_match.group(1))
        
    # 3. Całkowity czas uczenia (suma z train i eval)
    train_times = re.findall(r'training \[time: ([\d\.]+)s', content)
    eval_times = re.findall(r'evaluating \[time: ([\d\.]+)s', content)
    
    total_time = sum(float(t) for t in train_times) + sum(float(t) for t in eval_times)
    
    return {
        'model': model_name,
        'curve': curve,
        'test_ndcg': test_ndcg,
        'time_s': total_time
    }

def plot_learning_curves(parsed_data):
    curves = {d['model']: d['curve'] for d in parsed_data if d['curve']}
    
    if not curves:
        print("Nie znaleziono krzywych uczenia w folderach best_param!")
        return
        
    plt.figure(figsize=(10, 6))
    
    colors = {'BPR': '#2ca02c', 'NeuMF': '#ff7f0e', 'LightGCN': '#1f77b4', 'ItemKNN': '#d62728'}
    
    for m, curve in curves.items():
        # ItemKNN ma zwykle tylko 1 epokę ewaluacji, krzywa nie ma wielkiego sensu
        if m == 'ItemKNN' and len(curve) <= 1:
            continue 
        plt.plot(range(1, len(curve) + 1), curve, label=m, linewidth=2.5, color=colors.get(m))
        
    plt.title('Krzywe zbieżności na zbiorze walidacyjnym (NDCG@10)', fontsize=14)
    plt.xlabel('Epoka', fontsize=12)
    plt.ylabel('Valid NDCG@10', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(OUTPUT_IMG), exist_ok=True)
    plt.savefig(OUTPUT_IMG, dpi=300)
    print(f"Zapisano krzywe uczenia do {OUTPUT_IMG}")

def plot_time_vs_ndcg(parsed_data):
    # Wybieramy tylko te, które mają i czas i test_ndcg
    scatter_data = [d for d in parsed_data if d['test_ndcg'] is not None and d['time_s'] > 0]
    
    if not scatter_data:
        print("Brak danych do wykresu Time vs NDCG")
        return
        
    plt.figure(figsize=(10, 6))
    
    colors = {'ItemKNN': '#d62728', 'BPR': '#2ca02c', 'NeuMF': '#ff7f0e', 'LightGCN': '#1f77b4'}
    
    for d in scatter_data:
        plt.scatter(d['time_s'], d['test_ndcg'], 
                    s=500, label=d['model'], alpha=0.8, 
                    color=colors.get(d['model'], 'black'),
                    edgecolors='white', linewidth=2)
        plt.annotate(d['model'], (d['time_s'], d['test_ndcg'] + 0.001), 
                     ha='center', fontsize=12, fontweight='bold')
                     
    plt.title('Trade-off: Koszt obliczeniowy a trafność predykcji', fontsize=14)
    plt.xlabel('Czas pojedynczego pełnego treningu (sekundy)', fontsize=12)
    plt.ylabel('Test NDCG@10', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.legend(scatterpoints=1, frameon=True, labelspacing=1, title='Algorytmy')
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(OUTPUT_SCATTER), exist_ok=True)
    plt.savefig(OUTPUT_SCATTER, dpi=300)
    print(f"Zapisano wykres Trade-off do {OUTPUT_SCATTER}")

if __name__ == '__main__':
    parsed = []
    for m in MODELS:
        data = parse_best_param_log(m)
        if data:
            parsed.append(data)
            print(f"[{m}] Wczytano dane z best_param (Epoki: {len(data['curve'])}, Test NDCG: {data['test_ndcg']}, Czas: {data['time_s']}s)")
        else:
            print(f"[{m}] Brak logów w folderze best_param")
            
    if parsed:
        plot_learning_curves(parsed)
        plot_time_vs_ndcg(parsed)
    else:
        print("Nie znaleziono żadnych logów w folderach best_param!")
