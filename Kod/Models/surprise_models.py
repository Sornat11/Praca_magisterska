from surprise import SVD, KNNBasic
from .base_model import BaseModel

class SurpriseSVDModel(BaseModel):
    """
    SVD (Singular Value Decomposition) - Faktoryzacja macierzy.
    Działa poprzez rozkład macierzy ocen na dwie mniejsze macierze:
    jedną reprezentującą cechy użytkowników i drugą cechy produktów.
    """
    def __init__(self, n_factors=100, n_epochs=20):
        super().__init__("Surprise_SVD")
        self.model = SVD(n_factors=n_factors, n_epochs=n_epochs)

    def train(self, trainset):
        self.model.fit(trainset)

    def predict(self, user_id, item_id):
        # Surprise używa wewnętrznych surowych ID (raw_id)
        prediction = self.model.predict(str(user_id), str(item_id))
        return prediction.est

class SurpriseKNNModel(BaseModel):
    """
    KNN (K-Nearest Neighbors) - Filtrowanie współpracujące oparte na sąsiedztwie.
    Szuka 'K' najbardziej podobnych użytkowników i na podstawie ich ocen
    rekomenduje produkt.
    """
    def __init__(self, k=40, sim_options={'name': 'cosine', 'user_based': True}):
        super().__init__("Surprise_KNN")
        self.model = KNNBasic(k=k, sim_options=sim_options)

    def train(self, trainset):
        self.model.fit(trainset)

    def predict(self, user_id, item_id):
        prediction = self.model.predict(str(user_id), str(item_id))
        return prediction.est
