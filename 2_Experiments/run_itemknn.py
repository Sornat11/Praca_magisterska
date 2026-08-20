from recbole.quick_start import run_recbole
import os

if __name__ == '__main__':
    config_file_list = ['2_Experiments/Configs/itemknn.yaml']
    
    result = run_recbole(
        model='ItemKNN', 
        dataset='ml-100k', 
        config_file_list=config_file_list,
        config_dict={
            'checkpoint_dir': '3_Evaluation/Saved/'
        }
    )
    
    print("\n=== Wyniki końcowe ItemKNN (Baseline) ===")
    print(f"NDCG@10: {result['test_result']['ndcg@10']:.4f}")
    print(f"Hit@10:  {result['test_result']['hit@10']:.4f}")
