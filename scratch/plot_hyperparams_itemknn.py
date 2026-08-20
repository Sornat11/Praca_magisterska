import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'serif'
ACADEMIC_BLUE = '#1f77b4'

def parse_result_file(file_path):
    data = []
    with open(file_path, 'r') as f:
        content = f.read().strip().split('\n\n')
        for block in content:
            lines = block.strip().split('\n')
            if len(lines) < 3: continue
            
            params_str = lines[0]
            params = {}
            for param in params_str.split(','):
                k, v = param.strip().split(':')
                try:
                    params[k] = float(v)
                except ValueError:
                    params[k] = v
            
            valid_line = lines[2]
            match = re.search(r'ndcg@10\s*:\s*([0-9.]+)', valid_line)
            if match:
                ndcg = float(match.group(1))
                params['ndcg@10'] = ndcg
                data.append(params)
    return pd.DataFrame(data)

def generate_plots():
    df = parse_result_file('3_Evaluation/Reports/hyper_results_itemknn.result')
    if df.empty:
        print("Brak danych do wygenerowania wykresu.")
        return
        
    df = df.sort_values('k')
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['k'], df['ndcg@10'], marker='o', linestyle='-', color=ACADEMIC_BLUE, linewidth=2, markersize=8)
    
    # Zaznaczenie punktu maximum
    max_row = df.loc[df['ndcg@10'].idxmax()]
    plt.plot(max_row['k'], max_row['ndcg@10'], marker='*', color='red', markersize=15, label=f"Max NDCG ({max_row['ndcg@10']:.4f}) przy K={int(max_row['k'])}")
    
    plt.title('Wpływ rozmiaru sąsiedztwa (K) na miarę NDCG@10 (ItemKNN)', pad=20, fontsize=14)
    plt.xlabel('Liczba sąsiadów (K)', fontsize=12)
    plt.ylabel('NDCG@10', fontsize=12)
    plt.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig('Latex/img/hyper_itemknn_line.pdf', bbox_inches='tight')
    plt.savefig('Latex/img/hyper_itemknn_line.png', bbox_inches='tight', dpi=300)
    print("Wygenerowano wykres liniowy dla ItemKNN (Latex/img/hyper_itemknn_line.pdf)")

if __name__ == '__main__':
    generate_plots()
