import argparse
import sys
import yaml
import time
from typing import Optional, Dict, Any, List

import utils.recbole_patch

# Aktywujemy łatki ręcznie tylko dla strojenia hiperparametrów (omija błędy LightGBM/SciPy)
utils.recbole_patch.apply_patches()

from recbole.trainer import HyperTuning
from recbole.quick_start import objective_function as recbole_objective_function

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Strojenie hiperparametrow dla wybranego modelu.")
    parser.add_argument("--model", type=str, required=True, help="Nazwa modelu, np. BPR, LightGCN")
    parser.add_argument("--config", type=str, required=True, help="Sciezka do configu .yaml")
    parser.add_argument("--hyper", type=str, required=True, help="Sciezka do parametrow .hyper")
    parser.add_argument("--algo", type=str, default='bayes', help="Algorytm przeszukiwania, np. bayes, random")
    return parser.parse_args()

def objective_function(config_dict: Optional[Dict[str, Any]] = None, config_file_list: Optional[List[str]] = None, saved: bool = True) -> Any:
    fixed_config = {
        'checkpoint_dir': '3_Evaluation/Saved/',
        'state': 'INFO',
        'use_gpu': True,
        'gpu_id': '0',
        'device': 'cuda'
    }
    if config_dict is None:
        config_dict = {}
    config_dict.update(fixed_config)
    return recbole_objective_function(
        config_dict=config_dict, 
        config_file_list=config_file_list,
        saved=saved
    )

if __name__ == '__main__':
    args = parse_args()
    
    # Hack: Czyszczenie sys.argv przed inicjalizacją RecBole
    # Zapobiega błędom o nieznanych argumentach zgłaszanym przez parser wewnątrz RecBole.
    sys.argv[1:] = []
    
    dataset_name = 'unknown'
    with open(args.config, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
        if isinstance(config_data, dict):
            dataset_name = config_data.get('dataset', 'unknown')

    import datetime
    timestamp = datetime.datetime.now().strftime("%b-%d-%Y_%H-%M-%S")
    output_file = f'3_Evaluation/Reports/hyper_results_{args.model.lower()}_{dataset_name}_{args.algo}_{timestamp}.result'

    hp = HyperTuning(
        objective_function,
        algo=args.algo,
        max_evals=30, 
        params_file=args.hyper,
        fixed_config_file_list=[args.config]
    )

    print(f"Rozpoczynam optymalizację parametrów dla modelu: {args.model} algorytmem: {args.algo}")
    start_time = time.time()
    hp.run()
    end_time = time.time()
    total_time = end_time - start_time
    
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    hp.export_result(output_file)
    
    # Wyciąganie bloku z najlepszym wynikiem
    best_result_text = ""
    try:
        if hasattr(hp, 'best_params'):
            params_str = hp.params2str(hp.best_params)
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()
            blocks = content.split("\n\n")
            for block in blocks:
                if params_str in block:
                    best_result_text = block.strip()
                    break
    except Exception as e:
        pass
    
    # Dopisywanie czasu i podsumowania do pliku wyników
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(f"\n'Optimization_Time_Seconds': {total_time}\n")
        if best_result_text:
            f.write(f"\n=== NAJLEPSZY WYNIK ===\n{best_result_text}\n")
    
    print(f"\nOptymalizacja zakończona!")
    if hasattr(hp, 'best_params'):
        print(f"Najlepsze parametry: {hp.best_params}")
    if best_result_text:
        print(f"\n=== NAJLEPSZY WYNIK ===\n{best_result_text}")
    print(f"\nWyniki zapisano w: {output_file}")
