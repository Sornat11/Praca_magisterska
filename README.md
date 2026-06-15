# Porównanie algorytmów rekomendacyjnych - Praca Magisterska

Repozytorium zawiera kod źródłowy i eksperymenty do pracy magisterskiej dotyczącej porównania algorytmów filtrowania kolaboracyjnego, uczenia głębokiego oraz grafowych sieci neuronowych na przykładzie serwisu VOD.

## Struktura projektu

- `Kod/` - Główny pakiet z logiką systemów:
  - `DataSource/` - Pobieranie i przetwarzanie zbiorów MovieLens (oceny + metadane).
  - `Models/` - Implementacje modeli (SVD, KNN, planowane NCF, GNN).
  - `Utils/` - Narzędzia pomocnicze (ładowanie danych, transformacje).
- `Notebooks/` - Interaktywne eksperymenty i wizualizacje:
  - `eda_analysis.ipynb` - **Eksploracyjna Analiza Danych (EDA)**, statystyki demograficzne i gatunkowe.
  - `collaborative_filtering.ipynb` - Implementacja i ewaluacja klasycznych metod CF (SVD, KNN).
- `data/` - Pobrane dane w formacie CSV (ignorowane przez Git).
- `venv_thesis/` - Główne środowisko wirtualne projektu (ignorowane przez Git).

## Instalacja i konfiguracja

1. **Tworzenie środowiska:**
   ```bash
   python -m venv venv_thesis
   ```

2. **Aktywacja środowiska:**
   - **PowerShell:** `.\venv_thesis\Scripts\Activate.ps1`
   - **CMD:** `.\venv_thesis\Scripts\activate.bat`

3. **Instalacja bibliotek:**
   ```bash
   pip install -r requirements.txt
   ```

## Uruchamianie

### 1. Pobieranie danych
Projekt wymaga pobrania danych MovieLens wraz z metadanymi. Uruchom skrypt:
```bash
python Kod/DataSource/import_dataset.py
```
Możesz wybrać wersję **100k** (do szybkich testów) lub **1M** (do wyników końcowych).

### 2. Analiza i badania
Uruchamiaj notebooki w folderze `Notebooks/` w następującej kolejności:
1. `eda_analysis.ipynb` - Aby zrozumieć strukturę danych i wygenerować wykresy do pracy.
2. `collaborative_filtering.ipynb` - Aby wytrenować pierwsze modele (SVD/KNN).

**Ważne:** Upewnij się, że w Jupyter Notebook jako Kernel wybrane jest środowisko `venv_thesis`.

## Zarządzanie plikami
Zbiory danych (`data/`), literatura (`Materials/`) oraz pliki robocze pracy (`*.docx`, `*.pdf`) są ignorowane przez Git, aby utrzymać repozytorium lekkim i chronić treść rozprawy.

## Autor
Jakub Sornat  
Kierunek: Informatyka i Ekonometria
