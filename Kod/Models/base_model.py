from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    Abstrakcyjna klasa bazowa dla wszystkich modeli rekomendacyjnych.
    Zapewnia spójny interfejs: fit() do trenowania i predict() do prognozowania.
    """
    
    def __init__(self, name):
        self.name = name
        self.model = None

    @abstractmethod
    def train(self, trainset):
        """
        Trenuje model na dostarczonym zbiorze danych.
        trainset: Obiekt zbioru treningowego (specyficzny dla biblioteki).
        """
        pass

    @abstractmethod
    def predict(self, user_id, item_id):
        """
        Przewiduje ocenę (rating) dla danego użytkownika i produktu.
        """
        pass

    def __str__(self):
        return self.name
