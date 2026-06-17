from recbole.quick_start import run_recbole
import os

if __name__ == '__main__':
    # Uruchomienie RecBole z plikiem konfiguracyjnym
    config_file_list = ['2_Experiments/Configs/bpr.yaml']
    
    # run_recbole automatycznie zajmie się wszystkim: 
    # od ładowania danych po ewaluację
    result = run_recbole(
        model='BPR', 
        dataset='ml-1m', 
        config_file_list=config_file_list,

        config_dict={
            'checkpoint_dir': '3_Evaluation/Saved/'
        }
    )

    
    print("\n=== Wyniki końcowe BPR-MF (Baseline) ===")
    print(f"NDCG@10: {result['test_result']['ndcg@10']:.4f}")
    print(f"Hit@10:  {result['test_result']['hit@10']:.4f}")
