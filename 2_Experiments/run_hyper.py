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
        'state': 'INFO'
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

    output_file = f'3_Evaluation/Reports/hyper_results_{args.model.lower()}_{dataset_name}_{args.algo}.result'

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
    
    hp.export_result(output_file)
    
    # Dopisywanie czasu do pliku wyników
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(f"\n'Optimization_Time_Seconds': {total_time}\n")
    
    print(f"\nOptymalizacja zakończona!")
    if hasattr(hp, 'best_params'):
        print(f"Najlepsze parametry: {hp.best_params}")
    print(f"Wyniki zapisano w: {output_file}")
