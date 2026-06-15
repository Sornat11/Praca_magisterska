# Moduł DataSource

Ten folder zawiera narzędzia do pozyskiwania i wstępnego przygotowania danych do eksperymentów.

## Zawartość
- `import_dataset.py` - Skrypt do pobierania zbiorów MovieLens bezpośrednio ze strony GroupLens i ich przetwarzania na wygodne do analizy formaty przy użyciu biblioteki `pandas`.
- `data/` - Folder (tworzony automatycznie), w którym przechowywane są pobrane archiwa, oryginalne pliki zbiorów oraz wynikowe pliki CSV.

## Instrukcja pobierania danych
Aby pobrać dane, użyj głównego środowiska wirtualnego projektu:

```powershell
.\venv_thesis\Scripts\python.exe Kod/DataSource/import_dataset.py
```

Skrypt jest interaktywny i pozwala wybrać pomiędzy:
1. **MovieLens 100k** (do szybkich testów, zawiera oceny oraz pełne metadane filmów i użytkowników)
2. **MovieLens 1M** (do ostatecznych wyników i testów skalowalności, zawiera oceny oraz metadane)

Niezależnie od wyboru, skrypt pobierze archiwum ZIP, wypakuje je, a następnie wyodrębni i utworzy trzy ustandaryzowane pliki CSV:
- `movielens_[wersja]_ratings.csv` – tabela ocen (zawiera m.in. id użytkownika, id filmu i ocenę)
- `movielens_[wersja]_items.csv` – tabela z informacjami o filmach (tytuły, gatunki/metadane)
- `movielens_[wersja]_users.csv` – tabela z informacjami o użytkownikach (dane demograficzne)
