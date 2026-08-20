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
    df = parse_result_file('3_Evaluation/Reports/hyper_results_ncf.result')
    if df.empty:
        print("Brak danych do wygenerowania wykresu.")
        return
        
    df_agg = df.groupby(['learning_rate', 'dropout_prob'])['ndcg@10'].max().reset_index()
    pivot_df = df_agg.pivot(index='learning_rate', columns='dropout_prob', values='ndcg@10')
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_df, annot=True, cmap='YlGnBu', fmt='.4f', cbar_kws={'label': 'NDCG@10'})
    plt.title('Wpływ Dropout i współczynnika uczenia na miarę NDCG@10 (Model NCF)', pad=20, fontsize=14)
    plt.xlabel('Prawdopodobieństwo odrzucenia (Dropout Prob)', fontsize=12)
    plt.ylabel('Współczynnik uczenia (Learning Rate)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('Latex/img/hyper_ncf_heatmap.pdf', bbox_inches='tight')
    plt.savefig('Latex/img/hyper_ncf_heatmap.png', bbox_inches='tight', dpi=300)
    print("Wygenerowano wykres mapy ciepła dla NCF (Latex/img/hyper_ncf_heatmap.pdf)")

if __name__ == '__main__':
    generate_plots()
