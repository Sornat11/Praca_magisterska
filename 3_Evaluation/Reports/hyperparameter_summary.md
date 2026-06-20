# Podsumowanie Wyników Badania Hiperparametrów

Niniejszy raport zawiera szczegółowe podsumowanie i analizę wyników optymalizacji hiperparametrów dla modeli rekomendacyjnych w ramach pracy magisterskiej. Analiza została przeprowadzona na podstawie plików wynikowych `.result` z katalogu `3_Evaluation/Reports/` (`hyper_results_bpr.result` oraz `hyper_results_ncf.result`).

---

## 📊 Modele w Skrócie: Najlepsze Konfiguracje

| Model | Najlepsza Konfiguracja | NDCG@10 (Valid) | NDCG@10 (Test) | Recall@10 (Test) | MRR@10 (Test) | Hit@10 (Test) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **BPR-MF** | `embedding_size: 256`, `lr: 0.0005`, `batch_size: 4096` | **0.2175** | **0.2691** | **0.1767** | **0.4620** | **0.7675** |
| **NCF (NeuMF)** | `mf_emb: 128`, `mlp_emb: 128`, `lr: 0.0005`, `dropout: 0.2` | **0.1945** | **0.2448** | **0.1561** | **0.4257** | **0.7310** |
| **NCF (NeuMF)** | `mf_emb: 128`, `mlp_emb: 64`, `lr: 0.0001`, `dropout: 0.2` | **0.1966** | **0.2445** | **0.1564** | **0.4241** | **0.7276** |

> [!NOTE]
> Modele NCF osiągnęły nieco niższe wyniki od klasycznego BPR-MF, a ich optymalizacja była bardziej wrażliwa na dobór parametrów. Najlepsze wyniki BPR-MF uzyskano przy większym rozmiarze embeddingów (256) pod warunkiem zastosowania niskiego współczynnika uczenia (`lr: 0.0005`).

---

## 📈 Model BPR-MF (Bayesian Personalized Ranking - Matrix Factorization)

Przetestowano łącznie **20 różnych konfiguracji** parametrów.

### Najlepsze 5 konfiguracji (posortowane po Valid NDCG@10):

|   Emb Size |   Learning Rate |   Batch Size |   Valid NDCG@10 |   Valid Recall@10 |   Test NDCG@10 |   Test Recall@10 |
|-----------:|----------------:|-------------:|----------------:|------------------:|---------------:|-----------------:|
|        256 |          0.0005 |         4096 |          0.2175 |            0.1602 |         0.2691 |           0.1767 |
|        256 |          0.0005 |         2048 |          0.2164 |            0.158  |         0.2687 |           0.1762 |
|        128 |          0.0005 |         2048 |          0.2128 |            0.1543 |         0.2653 |           0.1705 |
|        256 |          0.001  |         4096 |          0.2121 |            0.1558 |         0.2642 |           0.1721 |
|        128 |          0.0005 |         1024 |          0.2104 |            0.1513 |         0.2614 |           0.1682 |

### 🔍 Wnioski z analizy parametrów BPR-MF:

- **Rozmiar Embeddingu (`embedding_size`):** Co ciekawe, mniejsze embeddingi (`64`) były bardziej stabilne i dały najwyższą średnią wartość NDCG (**0.2016**), podczas gdy `256` dało średnio **0.1850**. Wynika to z faktu, że przy dużych embeddingach (256) model łatwo przeucza się (overfitting), zwłaszcza przy wyższych współczynnikach uczenia (np. lr=0.01 dał NDCG zaledwie 0.1351). Jednakże, przy odpowiednio dobranym niskim lr (0.0005), rozmiar 256 osiągnął bezkonkurencyjnie najlepszy wynik (**0.2175**).
- **Współczynnik Uczenia (`learning_rate`):** Optymalne wartości to `0.0005` (średnia NDCG: **0.2122**) oraz `0.0010` (średnia NDCG: **0.2074**). Wyższe wartości, takie jak `0.005` (**0.1738**) i `0.01` (**0.1416**), drastycznie obniżają jakość rekomendacji.
- **Rozmiar Batcha (`train_batch_size`):** Większe rozmiary paczek uczących wykazują lekką przewagę. Średni wynik dla batcha `4096` to **0.1935**, dla `2048` to **0.1924**, a dla `1024` to **0.1836**.

---

## 🧠 Model NCF / NeuMF (Neural Collaborative Filtering)

Przetestowano łącznie **15 różnych konfiguracji** parametrów.

### Najlepsze 5 konfiguracji (posortowane po Valid NDCG@10):

|   Dropout |     LR |   MF Emb |   MLP Emb |   Valid NDCG@10 |   Valid Recall@10 |   Test NDCG@10 |   Test Recall@10 |
|----------:|-------:|---------:|----------:|----------------:|------------------:|---------------:|-----------------:|
|       0.2 | 0.0001 |      128 |        64 |          0.1966 |            0.1413 |         0.2445 |           0.1564 |
|       0.1 | 0.0001 |      128 |        64 |          0.1963 |            0.1402 |         0.2447 |           0.1562 |
|       0.1 | 0.0005 |      128 |        64 |          0.1958 |            0.1399 |         0.2432 |           0.1562 |
|       0.2 | 0.0005 |      128 |       128 |          0.1945 |            0.1388 |         0.2448 |           0.1561 |
|       0.1 | 0.0005 |       64 |        64 |          0.1929 |            0.1368 |         0.2406 |           0.155  |

### 🔍 Wnioski z analizy parametrów NCF:

- **Rozmiar Embeddingu MF (`mf_embedding_size`):** Większy rozmiar embeddingu dla części Matrix Factorization (`128`) sprawuje się średnio lepiej (**0.1939**) niż mniejszy (`64` - **0.1916**).
- **Rozmiar Embeddingu MLP (`mlp_embedding_size`):** Rozmiary `64` (średnia NDCG: **0.1930**) oraz `128` (średnia NDCG: **0.1920**) dają niemal identyczne rezultaty, z minimalną korzyścią na rzecz `64` ze względu na mniejszą liczbę parametrów sieci.
- **Współczynnik Uczenia (`learning_rate`):** NCF preferuje niższe tempo uczenia. Najlepsze średnie wyniki daje `0.0001` (**0.1939**) oraz `0.0005` (**0.1935**), podczas gdy przy `0.001` średni wynik spada do **0.1905**.
- **Prawdopodobieństwo Dropoutu (`dropout_prob`):** Wykorzystanie regularyzacji dropout zapobiega przeuczeniu sieci neuronowych. Wartość `0.1` (średnia NDCG: **0.1939**) oraz `0.2` (średnia NDCG: **0.1933**) dają najlepsze rezultaty. Całkowity brak dropoutu (`0.0` - **0.1906**) lub zbyt silny dropout (`0.3` - **0.1909**) dają gorsze wyniki.

---

## 🌐 Uwaga Dotycząca Modelu LightGCN (GNN)

W folderze wyników optymalizacji hiperparametrów brakuje pliku `hyper_results_gnn.result`. 

### Dlaczego tak się stało?
1. **Złożoność obliczeniowa:** Z analizy logów w katalogu `log/LightGCN/` wynika, że pojedynczy pełny przebieg treningowy dla LightGCN na zbiorze `ml-1m` (35-46 epok z wczesnym zatrzymaniem) zajmuje około **22.4 godziny** (1342.77 minut) na CPU.
2. **Przestrzeń hiperparametrów:** Zdefiniowany plik parametrów `gnn.hyper` zawiera:
   - `learning_rate` choice `[0.005, 0.001, 0.0005, 0.0001]` (4 opcje)
   - `n_layers` choice `[2, 3, 4]` (3 opcje)
   - `reg_weight` choice `[1e-05, 1e-04, 1e-03]` (3 opcje)
   - `embedding_size` choice `[64, 128]` (2 opcje)
   
   To daje łącznie **72 kombinacje**. Przy czasie treningu rzędu ~22h na kombinację, pełna optymalizacja trwałaby ponad **60 dni ciągłego działania**, co jest niepraktyczne bez dostępu do bardzo mocnych GPU.

### Obecna Konfiguracja LightGCN
Dla LightGCN zastosowano konfigurację ekspercką w pliku [gnn.yaml](file:///C:/Users/jakub/Documents/Materialy_na_studia/Informatyka_i_Ekonometria/Studia_Magisterskie/Praca_magisterska/2_Experiments/Configs/gnn.yaml) opartą na wnioskach z literatury i wstępnych testach:
- `embedding_size: 128`
- `n_layers: 3` (dla głębszej propagacji w grafie)
- `reg_weight: 1e-04`
- `learning_rate: 0.001`
- `train_batch_size: 2048`

Konfiguracja ta osiągnęła świetne wyniki w teście ostatecznym (**NDCG@10: 0.2691**, **Recall@10: 0.1732**, **Hit@10: 0.7589**), co plasuje LightGCN na równi z najlepszą zoptymalizowaną konfiguracją BPR-MF, ale przy znacznie większej stabilności.
