import argparse
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd

# Aktywujemy łatki (omija błędy NumPy i PyTorch 2.6)
import utils.recbole_patch
utils.recbole_patch.apply_patches()

from recbole.quick_start import run_recbole

def parse_args():
    parser = argparse.ArgumentParser(description="Testowanie wpływu pojedynczego parametru na model.")
    parser.add_argument("--model", type=str, required=True, help="Nazwa modelu, np. LightGCN")
    parser.add_argument("--dataset", type=str, required=True, help="Nazwa zbioru danych, np. ml-100k")
    parser.add_argument("--config", type=str, required=True, help="Ścieżka do pliku konfiguracyjnego .yaml")
    parser.add_argument("--param", type=str, required=True, help="Nazwa badanego parametru, np. n_layers")
    parser.add_argument("--values", type=str, nargs="+", required=True, help="Wartości do przetestowania (oddzielone spacją)")
    parser.add_argument("--metric", type=str, default="ndcg@10", help="Metryka rysowana na osi Y")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Czyszczenie argumentów sys.argv zapobiega błędom parsera wbudowanego w RecBole
    sys.argv[1:] = [] 
    
    results = []
    
    # Rozpoznawanie typów wartości (aby n_layers=2 było liczbą całkowitą, a lr=0.01 ułamkiem)
    parsed_values = []
    for v in args.values:
        try:
            if "." in v: parsed_values.append(float(v))
            else: parsed_values.append(int(v))
        except ValueError:
            parsed_values.append(v)

    print(f"Rozpoczynam badanie parametru '{args.param}' dla wartości: {parsed_values}")
    
    for val in parsed_values:
        print(f"\n{'='*50}")
        print(f"Testuję model z parametrem {args.param} = {val}")
        print(f"{'='*50}\n")
        
        config_dict = {
            args.param: val,
            'checkpoint_dir': '3_Evaluation/Saved/',
            'state': 'INFO',
            'use_gpu': True,
            'gpu_id': '0',
            'device': 'cuda'
        }
        
        # Uruchamiamy pełny cykl RecBole dla danej wartości (bez śmiecenia dysku zapisanymi modelami)
        result_dict = run_recbole(
            model=args.model,
            dataset=args.dataset,
            config_file_list=[args.config],
            config_dict=config_dict,
            saved=False
        )
        
        # Z RecBole wyciągamy ostateczny słownik z wynikami ze zbioru testowego
        test_res = result_dict.get('test_result', {})
        
        score = test_res.get(args.metric, 0.0)
        
        results.append({
            args.param: val,
            args.metric: float(score),
            'full_results': test_res
        })
        
    # Tworzenie czytelnego podsumowania
    df = pd.DataFrame(results)
    print("\n\n" + "="*50)
    print("=== PODSUMOWANIE EKSPERYMENTU ===")
    print("="*50)
    print(df[[args.param, args.metric]])
    
    # Zapisywanie wyników do pliku CSV
    os.makedirs('3_Evaluation/Reports/', exist_ok=True)
    report_file = f'3_Evaluation/Reports/sweep_{args.model.lower()}_{args.param}.csv'
    df.to_csv(report_file, index=False)
    print(f"\nSurowe wyniki zapisano do pliku: {report_file}")
    
    # Generowanie ładnego wykresu (wyciągamy same wartości z numpy floats)
    plt.figure(figsize=(9, 6))
    
    x_vals = [str(v) for v in df[args.param]]
    y_vals = [float(v) for v in df[args.metric]]
    
    plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='#1f77b4', linewidth=2, markersize=8)
    plt.title(f"Wpływ parametru '{args.param}' na metrykę {args.metric}\n(Model: {args.model}, Zbiór: {args.dataset})", fontsize=14, pad=15)
    plt.xlabel(f"Wartość {args.param}", fontsize=12)
    plt.ylabel(args.metric, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Odrobina marginesu żeby kropki nie przyklejały się do krawędzi wykresu
    plt.margins(0.1)
    
    plot_file = f'3_Evaluation/Reports/sweep_{args.model.lower()}_{args.param}.png'
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"Wykres zapisano do pliku: {plot_file}")

if __name__ == "__main__":
    main()
