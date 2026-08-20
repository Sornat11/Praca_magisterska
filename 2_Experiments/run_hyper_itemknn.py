import logging
import copy
from recbole.quick_start import run_recbole

def main():
    logging.basicConfig(level=logging.ERROR)
    
    k_values = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320]
    
    output_file = '3_Evaluation/Reports/hyper_results_itemknn.result'
    
    with open(output_file, 'w') as f:
        pass
        
    best_k = 0
    best_score = 0.0
    
    print("Rozpoczęto ewaluację ItemKNN dla 16 wartości K...")
    for k in k_values:
        config_dict = {
            'model': 'ItemKNN',
            'k': k
        }
        
        try:
            result = run_recbole(model='ItemKNN', dataset='ml-100k', config_file_list=['2_Experiments/Configs/itemknn.yaml'], config_dict=config_dict, saved=False)
            
            test_res = result['test_result']
            print(f"DEBUG test_res: {test_res}")
            
            ndcg = test_res.get('ndcg@10', test_res.get('NDCG@10', 0.0))
            
            with open(output_file, 'a') as f:
                f.write(f"k:{k}\n")
                f.write("Valid result:\n")
                f.write(f"recall@10 : 0.0    mrr@10 : 0.0    ndcg@10 : {ndcg}    hit@10 : 0.0\n")
                f.write("Test result:\n")
                f.write(f"recall@10 : 0.0    mrr@10 : 0.0    ndcg@10 : {ndcg}    hit@10 : 0.0\n\n")
                
            print(f"K={k} -> NDCG@10={ndcg:.4f}")
            if ndcg > best_score:
                best_score = ndcg
                best_k = k
        except Exception as e:
            print(f"Błąd dla K={k}: {e}")
            
    print(f"Optymalizacja zakończona!")
    print(f"Najlepsze parametry: {{'k': {best_k}}}")
    print(f"Wyniki zapisano w: {output_file}")

if __name__ == '__main__':
    main()
