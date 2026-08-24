import os
import re
import glob
import pandas as pd

# Konfiguracja ścieżek
LOGS_DIR = 'log'
OUTPUT_TEX = 'Latex/tables/wyniki_eksperymentow.tex'
MODELS = ['ItemKNN', 'BPR', 'NeuMF', 'LightGCN']

def parse_test_results_from_log(model_name):
    search_path = os.path.join(LOGS_DIR, model_name, 'best_param', '*.log')
    log_files = glob.glob(search_path)
    
    if not log_files:
        return None
        
    # Wybierz najnowszy plik z logami (jeśli użytkownik uruchamiał go kilkukrotnie)
    latest_log = max(log_files, key=os.path.getmtime)
    
    with open(latest_log, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Szukamy bloku wyników testowych, typowo "test result: OrderedDict(...)"
    test_idx = content.find('test result:')
    if test_idx == -1:
        return None
        
    test_str = content[test_idx:]
    
    metrics = {}
    patterns = {
        'Recall@10': r'\'recall@10\':\s*([\d\.]+)',
        'MRR@10': r'\'mrr@10\':\s*([\d\.]+)',
        'NDCG@10': r'\'ndcg@10\':\s*([\d\.]+)',
        'Hit@10': r'\'hit@10\':\s*([\d\.]+)'
    }
    
    for metric_name, pattern in patterns.items():
        match = re.search(pattern, test_str)
        if match:
            metrics[metric_name] = float(match.group(1))
            
    if metrics:
        metrics['Model'] = model_name
        return metrics
    return None

def generate_latex():
    results = []
    
    for m in MODELS:
        res = parse_test_results_from_log(m)
        if res:
            results.append(res)
            print(f"[{m}] Załadowano finalne metryki ze zbioru testowego z best_param.")
        else:
            print(f"[{m}] Brak wyników testowych w folderze best_param!")
            
    if not results:
        print("Nie znaleziono wyników w żadnym z folderów best_param. Tabela nie została wygenerowana.")
        return
        
    df = pd.DataFrame(results)
    
    # Kolejność kolumn
    cols = ['Model', 'NDCG@10', 'Recall@10', 'Hit@10', 'MRR@10']
    
    # Zabezpieczenie na wypadek, gdyby brakowało jakiejś metryki
    for c in cols:
        if c not in df.columns:
            df[c] = 0.0
            
    df = df[cols]
    
    # Ustalenie odgórnej kolejności wierszy w tabeli (od najprostszego do najpotężniejszego modelu)
    model_order = {'ItemKNN': 0, 'BPR': 1, 'NeuMF': 2, 'LightGCN': 3}
    df['order'] = df['Model'].map(model_order)
    df = df.sort_values('order').drop('order', axis=1)
    
    # Generowanie kodu LaTeX 
    latex_lines = [
        "\\begin{tabular}{|l|c|c|c|c|}",
        "\\hline",
        "\\textbf{Model} & \\textbf{NDCG@10} & \\textbf{Recall@10} & \\textbf{Hit@10} & \\textbf{MRR@10} \\\\ \\hline"
    ]
    
    for _, row in df.iterrows():
        line_vals = [row['Model']]
        
        for col in cols[1:]:
            val = row[col]
            all_vals = sorted(df[col].unique(), reverse=True)
            max_val = all_vals[0] if len(all_vals) > 0 else -1
            runner_val = all_vals[1] if len(all_vals) > 1 else -1
            
            val_str = f"{val:.4f}"
            if val == max_val:
                val_str = f"\\textbf{{{val_str}}}"
            elif val == runner_val:
                val_str = f"\\underline{{{val_str}}}"
                
            line_vals.append(val_str)
            
        latex_lines.append(" & ".join(line_vals) + " \\\\ \\hline")
        
    latex_lines.append("\\end{tabular}")
    latex_code = "\n".join(latex_lines)
    
    os.makedirs(os.path.dirname(OUTPUT_TEX), exist_ok=True)
    with open(OUTPUT_TEX, 'w', encoding='utf-8') as f:
        f.write(latex_code)
        
    print(f"\nWygenerowano główną tabelę LaTeX w: {OUTPUT_TEX}")

if __name__ == '__main__':
    generate_latex()
