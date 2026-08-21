import argparse
import sys
import time

import utils.recbole_patch
utils.recbole_patch.apply_patches()
from recbole.quick_start import run_recbole

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trenowanie pojedynczego modelu RecBole.")
    parser.add_argument("--model", type=str, required=True, help="Nazwa modelu, np. BPR, LightGCN")
    parser.add_argument("--dataset", type=str, required=True, help="Nazwa datasetu, np. ml-100k")
    parser.add_argument("--config", type=str, required=True, help="Sciezka do configu .yaml")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    
    # Hack: RecBole automatycznie parsuje sys.argv, co wyrzuca błędy przy customowych argumentach.
    # Czyścimy sys.argv, aby tego uniknąć.
    sys.argv[1:] = []
    
    config_file_list = [args.config]
    
    start_time = time.time()
    
    result = run_recbole(
        model=args.model, 
        dataset=args.dataset, 
        config_file_list=config_file_list,
        config_dict={
            'checkpoint_dir': '3_Evaluation/Saved/'
        }
    )
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n=== Wyniki końcowe {args.model} ===")
    test_results = result.get('test_result', {})
    for metric, val in test_results.items():
        print(f"{metric}: {val:.4f}")
    
    print(f"Czas trenowania: {total_time:.2f} s")
