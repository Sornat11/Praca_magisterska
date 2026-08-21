import pandas as pd
import os

INPUT_DIR = '0_Raw_Data'
OUTPUT_DIR = 'Datasets'
DATASETS_TO_PROCESS = ['ml-100k', 'ml-1m']

def convert_to_inter(input_dir: str, output_dir: str, dataset_name: str) -> None:
    """
    Konwertuje pliki CSV z ocenami, użytkownikami i przedmiotami 
    na format Atomic (.inter, .user, .item) wymagany przez RecBole.
    """
    
    # --- 1. Oceny (Interakcje) ---
    ratings_csv = os.path.join(input_dir, f"movielens_{dataset_name.replace('ml-', '')}_ratings.csv")
    if not os.path.exists(ratings_csv):
        print(f"Error: {ratings_csv} nie istnieje.")
        return

    df_ratings = pd.read_csv(ratings_csv)
    target_path = os.path.join(output_dir, dataset_name)
    os.makedirs(target_path, exist_ok=True)
    
    inter_df = pd.DataFrame({
        'user_id:token': df_ratings['user_id'].astype(str),
        'item_id:token': df_ratings['item_id'].astype(str),
        'rating:float': df_ratings['rating'].astype(float),
        'timestamp:float': df_ratings['timestamp'].astype(float)
    })
    
    inter_file = os.path.join(target_path, f"{dataset_name}.inter")
    inter_df.to_csv(inter_file, sep='\t', index=False)
    print(f"Zapisano interakcje: {inter_file}")

    # --- 2. Użytkownicy (.user) ---
    users_csv = os.path.join(input_dir, f"movielens_{dataset_name.replace('ml-', '')}_users.csv")
    if os.path.exists(users_csv):
        df_users = pd.read_csv(users_csv)
        user_df = pd.DataFrame({
            'user_id:token': df_users['user_id'].astype(str),
            'age:token': df_users['age'].astype(str),
            'gender:token': df_users['gender'].astype(str),
            'occupation:token': df_users['occupation'].astype(str)
        })
        
        user_file = os.path.join(target_path, f"{dataset_name}.user")
        user_df.to_csv(user_file, sep='\t', index=False)
        print(f"Zapisano użytkowników: {user_file}")

    # --- 3. Przedmioty (.item) ---
    items_csv = os.path.join(input_dir, f"movielens_{dataset_name.replace('ml-', '')}_items.csv")
    if os.path.exists(items_csv):
        df_items = pd.read_csv(items_csv)
        item_df = pd.DataFrame()
        
        if dataset_name == 'ml-1m':
            # ML-1M ma gatunki w formacie 'Action|Comedy'
            item_df['item_id:token'] = df_items['movie_id'].astype(str)
            item_df['title:token'] = df_items['title'].astype(str)
            item_df['genres:token_seq'] = df_items['genres'].str.replace('|', ' ')
        else:
            # ML-100k
            item_df['item_id:token'] = df_items['movie_id'].astype(str)
            item_df['title:token'] = df_items['movie_title'].astype(str)
            
        item_file = os.path.join(target_path, f"{dataset_name}.item")
        item_df.to_csv(item_file, sep='\t', index=False)
        print(f"Zapisano przedmioty: {item_file}")

if __name__ == "__main__":
    for dataset_name in DATASETS_TO_PROCESS:
        print(f"\nRozpoczynam konwersję zbioru: {dataset_name}")
        convert_to_inter(
            input_dir=INPUT_DIR,
            output_dir=OUTPUT_DIR,
            dataset_name=dataset_name
        )
