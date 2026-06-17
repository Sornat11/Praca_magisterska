from recbole.quick_start import run_recbole
import os

if __name__ == '__main__':
    # Uruchomienie modelu NCF (NeuMF)
    # NeuMF łączy w sobie zalety klasycznej faktoryzacji (GMF) 
    # oraz nieliniowość sieci MLP.
    config_file_list = ['2_Experiments/Configs/ncf.yaml']
    
    result = run_recbole(
        model='NeuMF', 
        dataset='ml-1m', 
        config_file_list=config_file_list,
        config_dict={
            'checkpoint_dir': '3_Evaluation/Saved/'
        }
    )
    
    print("\n=== Wyniki końcowe NCF (NeuMF) ===")
    print(f"NDCG@10: {result['test_result']['ndcg@10']:.4f}")
    print(f"Hit@10:  {result['test_result']['hit@10']:.4f}")
