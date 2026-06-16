import numpy as np

def hit_ratio_at_k(recommended_items, relevant_items, k=10):
    """
    Oblicza Hit Ratio (HR@K).
    Zwraca 1, jeśli przynajmniej jeden relewantny element znajduje się 
    w top-K rekomendacji, 0 w przeciwnym razie.
    """
    recommended_k = recommended_items[:k]
    hits = set(recommended_k).intersection(set(relevant_items))
    return 1 if len(hits) > 0 else 0

def ndcg_at_k(recommended_items, relevant_items, k=10):
    """
    Oblicza Normalized Discounted Cumulative Gain (NDCG@K).
    Zwraca wyższy wynik (bliżej 1.0), jeśli relewantne elementy 
    znajdują się na wyższych (wcześniejszych) pozycjach na liście rekomendacji.
    """
    recommended_k = recommended_items[:k]
    dcg = 0.0
    idcg = 0.0
    
    # Obliczanie IDCG (Ideal DCG) - najlepszy możliwy scenariusz, 
    # gdzie wszystkie relewantne elementy zajmują pierwsze miejsca
    for i in range(min(len(relevant_items), k)):
        idcg += 1.0 / np.log2(i + 2)
        
    if idcg == 0.0:
        return 0.0
        
    # Obliczanie rzeczywistego DCG dla wygenerowanej listy rekomendacji
    for i, item in enumerate(recommended_k):
        if item in relevant_items:
            dcg += 1.0 / np.log2(i + 2)
            
    return dcg / idcg

def precision_at_k(recommended_items, relevant_items, k=10):
    """
    Oblicza Precision@K.
    Proporcja relewantnych elementów w top-K wygenerowanych rekomendacji.
    """
    recommended_k = recommended_items[:k]
    hits = set(recommended_k).intersection(set(relevant_items))
    return len(hits) / k

def recall_at_k(recommended_items, relevant_items, k=10):
    """
    Oblicza Recall@K.
    Proporcja wszystkich relewantnych elementów, które zostały odnalezione w top-K.
    """
    recommended_k = recommended_items[:k]
    hits = set(recommended_k).intersection(set(relevant_items))
    if len(relevant_items) == 0:
        return 0.0
    return len(hits) / len(relevant_items)
