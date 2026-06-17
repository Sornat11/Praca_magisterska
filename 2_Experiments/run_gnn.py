from recbole.quick_start import run_recbole
import os

if __name__ == '__main__':
    # Uruchomienie modelu LightGCN (Graph Neural Network)
    # LightGCN uczy się reprezentacji poprzez sploty na grafie 
    # dwudzielnym użytkownik-film.
    config_file_list = ['2_Experiments/Configs/gnn.yaml']
    
    result = run_recbole(
        model='LightGCN', 
        dataset='ml-1m', 
        config_file_list=config_file_list,
        config_dict={
            'checkpoint_dir': '3_Evaluation/Saved/'
        }
    )
    
    print("\n=== Wyniki końcowe LightGCN (GNN) ===")
    print(f"NDCG@10: {result['test_result']['ndcg@10']:.4f}")
    print(f"Hit@10:  {result['test_result']['hit@10']:.4f}")
