import pandas as pd
from surprise import Dataset, Reader
import os

def load_movielens_to_surprise(file_path=None, version='100k'):
    """
    Wczytuje dane MovieLens z pliku CSV.
    Jeśli file_path nie jest podany, szuka domyślnego pliku na podstawie wersji.
    """
    if file_path is None:
        # Próba znalezienia pliku w standardowej lokalizacji
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'DataSource', 'data', f'movielens_{version}.csv')
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Nie znaleziono pliku danych: {file_path}. "
                                f"Uruchom najpierw Kod/DataSource/import_dataset.py")

    df = pd.read_csv(file_path)
    
    # Reader musi znać skalę ocen (w MovieLens to 1-5)
    reader = Reader(rating_scale=(1, 5))
    
    # Kolumny muszą być w kolejności: user, item, rating
    data = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)
    
    return data
