from surprise.model_selection import train_test_split
from surprise import accuracy
from Kod.Utils.data_loader import load_movielens_to_surprise
from Kod.Models.surprise_models import SurpriseSVDModel, SurpriseKNNModel

def run_basic_experiment():
    print("--- Rozpoczynam eksperyment: Podstawowe Algorytmy ---")
    
    # 1. Załaduj dane
    print("\n[1/4] Ładowanie danych...")
    data = load_movielens_to_surprise()
    
    # 2. Podział na zbiór treningowy i testowy (80/20)
    # To kluczowe, żeby sprawdzić jak model radzi sobie z nowymi danymi
    print("[2/4] Podział danych na train/test...")
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
    
    # 3. Inicjalizacja modeli
    models = [
        SurpriseSVDModel(),
        SurpriseKNNModel()
    ]
    
    # 4. Trenowanie i ewaluacja
    print("[3/4] Trenowanie modeli...")
    for model_wrapper in models:
        print(f"\nUruchamiam: {model_wrapper.name}")
        
        # Trenowanie (na obiekcie Surprise)
        model_wrapper.train(trainset)
        
        # Testowanie (predykcja dla całego zbioru testowego)
        # Używamy bezpośrednio obiektu surprise.model do szybkiej ewaluacji
        predictions = model_wrapper.model.test(testset)
        
        # Metryka RMSE (Root Mean Squared Error)
        # Mówi nam o ile średnio "myli się" model w skali 1-5
        rmse = accuracy.rmse(predictions)
        print(f"Wynik RMSE dla {model_wrapper.name}: {rmse:.4f}")

    print("\n[4/4] Eksperyment zakończony.")

if __name__ == "__main__":
    run_basic_experiment()
