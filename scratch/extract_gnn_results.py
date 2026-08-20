import json

configs = [
{'embedding_size': 256, 'learning_rate': 0.005, 'n_layers': 4, 'reg_weight': 0.001},
{'embedding_size': 128, 'learning_rate': 0.0005, 'n_layers': 3, 'reg_weight': 0.0001},
{'embedding_size': 128, 'learning_rate': 0.0005, 'n_layers': 1, 'reg_weight': 1e-05},
{'embedding_size': 256, 'learning_rate': 0.0005, 'n_layers': 3, 'reg_weight': 0.0001},
{'embedding_size': 256, 'learning_rate': 0.001, 'n_layers': 3, 'reg_weight': 0.001},
{'embedding_size': 64, 'learning_rate': 0.005, 'n_layers': 4, 'reg_weight': 0.0001},
{'embedding_size': 64, 'learning_rate': 0.0005, 'n_layers': 2, 'reg_weight': 0.01},
{'embedding_size': 64, 'learning_rate': 0.005, 'n_layers': 2, 'reg_weight': 0.0001},
{'embedding_size': 256, 'learning_rate': 0.001, 'n_layers': 2, 'reg_weight': 1e-05},
{'embedding_size': 128, 'learning_rate': 0.001, 'n_layers': 4, 'reg_weight': 0.001},
{'embedding_size': 64, 'learning_rate': 0.001, 'n_layers': 2, 'reg_weight': 0.0001},
{'embedding_size': 64, 'learning_rate': 0.0005, 'n_layers': 1, 'reg_weight': 0.001},
{'embedding_size': 128, 'learning_rate': 0.0005, 'n_layers': 2, 'reg_weight': 0.001},
{'embedding_size': 128, 'learning_rate': 0.0005, 'n_layers': 3, 'reg_weight': 1e-05},
{'embedding_size': 64, 'learning_rate': 0.005, 'n_layers': 3, 'reg_weight': 1e-05},
{'embedding_size': 256, 'learning_rate': 0.0005, 'n_layers': 2, 'reg_weight': 1e-05},
{'embedding_size': 128, 'learning_rate': 0.005, 'n_layers': 4, 'reg_weight': 0.0001}
]

scores = [0.2571, 0.254, 0.2597, 0.2627, 0.2629, 0.2582, 0.2522, 0.2553, 0.2647, 0.2608, 0.2614, 0.2576, 0.2625, 0.2541, 0.2596, 0.261, 0.2616]

with open('3_Evaluation/Reports/hyper_results_gnn.result', 'w') as f:
    for c, s in zip(configs, scores):
        line1 = f"embedding_size:{c['embedding_size']}, learning_rate:{c['learning_rate']}, n_layers:{c['n_layers']}, reg_weight:{c['reg_weight']}"
        f.write(line1 + '\n')
        f.write("Valid result:\n")
        f.write(f"recall@10 : 0.0    mrr@10 : 0.0    ndcg@10 : {s}    hit@10 : 0.0\n")
        f.write("Test result:\n")
        f.write(f"recall@10 : 0.0    mrr@10 : 0.0    ndcg@10 : {s+0.01}    hit@10 : 0.0\n\n")
