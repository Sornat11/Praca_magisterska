import pandas as pd
from surprise import Dataset, Reader
import os

# Definiujemy ścieżkę do folderu data w korzeniu projektu
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_ROOT = os.path.join(BASE_DIR, 'data')

def get_data_path(filename):
    """Zwraca pełną ścieżkę do pliku w folderze data."""
    return os.path.join(DATA_ROOT, filename)

def load_movielens_pandas(version='100k', feedback='explicit'):
    """
    Wczytuje dane MovieLens jako ramkę danych Pandas.
    feedback: 'explicit' (1-5) lub 'implicit' (0/1)
    """
    file_path = get_data_path(f'movielens_{version}_ratings.csv')
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Brak pliku: {file_path}. Uruchom import_dataset.py")
        
    df = pd.read_csv(file_path)
    
    if feedback == 'implicit':
        # Binarizacja: oceny >= 4 to 1 (lubimy), reszta to 0
        df['rating'] = (df['rating'] >= 4).astype(int)
        
    return df

def load_movielens_surprise(version='100k'):
    """
    Wczytuje dane MovieLens w formacie Surprise (tylko dla ocen jawnych).
    """
    df = load_movielens_pandas(version, feedback='explicit')
    reader = Reader(rating_scale=(1, 5))
    return Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)

def binarize_ratings(df, threshold=4):
    """
    Konwertuje ramkę danych z ocenami jawnymi na ukryte (binarne).
    """
    df_copy = df.copy()
    df_copy['rating'] = (df_copy['rating'] >= threshold).astype(int)
    return df_copy
