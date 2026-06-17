import pandas as pd
import os

def convert_to_inter(input_csv, output_dir, dataset_name):
    """
    Konwertuje plik CSV z ocenami na format .inter wymagany przez RecBole.
    """
    if not os.path.exists(input_csv):
        print(f"Error: {input_csv} nie istnieje. Uruchom najpierw import_raw_data.py")
        return

    # Wczytanie danych
    df = pd.read_csv(input_csv)
    
    # RecBole wymaga specyficznych nazw kolumn i typów (format: name:type)
    # user_id:token, item_id:token, rating:float, timestamp:float
    
    # Tworzymy folder dla zbioru danych
    target_path = os.path.join(output_dir, dataset_name)
    os.makedirs(target_path, exist_ok=True)
    
    # Przygotowanie ramki danych pod format .inter
    inter_df = pd.DataFrame()
    inter_df['user_id:token'] = df['user_id'].astype(str)
    inter_df['item_id:token'] = df['item_id'].astype(str)
    inter_df['rating:float'] = df['rating'].astype(float)
    inter_df['timestamp:float'] = df['timestamp'].astype(float)
    
    # Zapis do pliku .inter (rozdzielany tabulatorem)
    output_file = os.path.join(target_path, f"{dataset_name}.inter")
    inter_df.to_csv(output_file, sep='\t', index=False)
    
    print(f"Sukces! Konwersja zakończona. Plik zapisany w: {output_file}")

if __name__ == "__main__":
    input_dir = '0_Raw_Data'
    output_dir = 'Datasets'
    
    files = [f for f in os.listdir(input_dir) if f.endswith('_ratings.csv')]
    
    if not files:
        print(f"Brak plików do konwersji w {input_dir}. Uruchom najpierw import_raw_data.py")
    
    for file in files:
        # Wyciągamy nazwę zbioru (np. movielens_100k)
        dataset_name = file.replace('_ratings.csv', '').replace('movielens_', 'ml-')
        
        print(f"\nRozpoczynam konwersję: {file} -> {dataset_name}")
        convert_to_inter(
            input_csv=os.path.join(input_dir, file),
            output_dir=output_dir,
            dataset_name=dataset_name
        )
