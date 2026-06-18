from recbole.trainer import HyperTuning
from recbole.quick_start import run_recbole

def objective_function(config_dict=None, config_file_list=None, saved=True):
    result = run_recbole(
        config_dict=config_dict, 
        config_file_list=config_file_list,
        saved=saved
    )
    return result['test_result']['ndcg@10']

if __name__ == '__main__':
    model_name = 'LightGCN'
    config_file_list = ['2_Experiments/Configs/gnn.yaml']
    params_file = '2_Experiments/Hyperparams/gnn.hyper'
    output_file = f'3_Evaluation/Reports/hyper_results_gnn.result'

    hp = HyperTuning(
        objective_function, 
        arg_dict={'config_file_list': config_file_list},
        params_file=params_file,
        fixed_config_dict={
            'checkpoint_dir': '3_Evaluation/Saved/',
            'state': 'INFO'
        }
    )

    print(f"Rozpoczynam optymalizację parametrów dla modelu: {model_name}")
    hp.run()
    hp.export_result(output_file)
    
    print(f"\nOptymalizacja zakończona!")
    print(f"Najlepsze parametry: {hp.best_params}")
    print(f"Wyniki zapisano w: {output_file}")
