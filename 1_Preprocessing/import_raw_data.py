import os
import zipfile
import urllib.request
import pandas as pd

def download_and_extract(url, zip_path, extract_path):
    if not os.path.exists(zip_path):
        print(f"Pobieranie {url}...")
        urllib.request.urlretrieve(url, zip_path)
    
    print(f"Rozpakowywanie do {extract_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def import_ml_100k():
    url = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
    zip_path = "0_Raw_Data/ml-100k.zip"
    extract_path = "0_Raw_Data/"
    
    download_and_extract(url, zip_path, extract_path)
    
    # Przetwarzanie ocen
    names = ['user_id', 'item_id', 'rating', 'timestamp']
    df_ratings = pd.read_csv('0_Raw_Data/ml-100k/u.data', sep='\t', names=names)
    df_ratings.to_csv('0_Raw_Data/movielens_100k_ratings.csv', index=False)
    
    # Przetwarzanie filmów (metadane)
    cols = "movie_id | movie_title | release_date | video_release_date | IMDb_URL | unknown | Action | Adventure | Animation | Children's | Comedy | Crime | Documentary | Drama | Fantasy | Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi | Thriller | War | Western"
    movie_cols = [c.strip() for c in cols.split('|')]
    df_items = pd.read_csv('0_Raw_Data/ml-100k/u.item', sep='|', names=movie_cols, encoding='latin-1')
    df_items.to_csv('0_Raw_Data/movielens_100k_items.csv', index=False)
    
    # Przetwarzanie użytkowników (metadane)
    user_cols = ['user_id', 'age', 'gender', 'occupation', 'zip_code']
    df_users = pd.read_csv('0_Raw_Data/ml-100k/u.user', sep='|', names=user_cols)
    df_users.to_csv('0_Raw_Data/movielens_100k_users.csv', index=False)
    
    print("\n[ML-100k] Sukces! Zapisano oceny, filmy i użytkowników.")

def import_ml_1m():
    url = "https://files.grouplens.org/datasets/movielens/ml-1m.zip"
    zip_path = "0_Raw_Data/ml-1m.zip"
    extract_path = "0_Raw_Data"
    
    download_and_extract(url, zip_path, extract_path)
    
    # Przetwarzanie ocen
    df_ratings = pd.read_csv('0_Raw_Data/ml-1m/ratings.dat', sep='::', names=['user_id', 'item_id', 'rating', 'timestamp'], engine='python')
    df_ratings.to_csv('0_Raw_Data/movielens_1m_ratings.csv', index=False)
    
    # Przetwarzanie filmów
    df_items = pd.read_csv('0_Raw_Data/ml-1m/movies.dat', sep='::', names=['movie_id', 'title', 'genres'], engine='python', encoding='latin-1')
    df_items.to_csv('0_Raw_Data/movielens_1m_items.csv', index=False)
    
    # Przetwarzanie użytkowników
    df_users = pd.read_csv('0_Raw_Data/ml-1m/users.dat', sep='::', names=['user_id', 'gender', 'age', 'occupation', 'zip_code'], engine='python')
    df_users.to_csv('0_Raw_Data/movielens_1m_users.csv', index=False)
    
    print("\n[ML-1m] Sukces! Zapisano oceny, filmy i użytkowników.")

if __name__ == "__main__":
    os.makedirs('0_Raw_Data', exist_ok=True)
    import_ml_100k()
    import_ml_1m()