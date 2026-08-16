# Konwencja notacji matematycznej dla pracy magisterskiej

Poniższe zasady notacji zostały przyjęte w celu zachowania spójności i matematycznego rygoru we wszystkich wzorach i objaśnieniach w pracy (szczególnie w rozdziale 2 i 3).

## 1. Skalary (Pojedyncze liczby, indeksy, stałe)
Zapisywane są w środowisku matematycznym zwykłą **kursywą (pochyłym eR/eX)**. Nie stosujemy pogrubienia.
* **Przykłady w LaTeX:** `$k$`, `$M$`, `$N$`, `$u$`, `$i$`, `$p_{uf}$`, `$\hat{x}_{ui}$`
* **Zastosowanie:** Indeksy użytkowników, wymiary macierzy, pojedyncze składowe wektora, wyestymowane pojedyncze oceny (scores), liczby skalarne.

## 2. Wektory (Tablice jednowymiarowe)
Zapisywane są **małą, pogrubioną** literą. W objaśnieniach (np. pod słowem "Gdzie:") również muszą zachować pogrubienie.
* **Przykłady w LaTeX:** `$\mathbf{p}_u$`, `$\mathbf{q}_i$`
* **Zastosowanie:** Cechy ukryte (embeddings) pojedynczego użytkownika lub obiektu, np. wektor reprezentujący gust usera $u$.

## 3. Macierze (Tablice dwuwymiarowe i wielowymiarowe)
Zapisywane są **wielką, pogrubioną** literą.
* **Przykłady w LaTeX:** `$\mathbf{R}$`, `$\mathbf{Y}$`, `$\mathbf{P}$`, `$\mathbf{Q}$`
* **Zastosowanie:** Macierz wszystkich interakcji, macierz wag wyuczonych osadzeń dla wszystkich obiektów w sieci.

## 4. Zbiory i przestrzenie
Zapisywane są przy użyciu dedykowanych krojów pism matematycznych (kaligraficznych lub tablicowych).
* **Zbiory obiektów (LaTeX):** `$\mathcal{U}$`, `$\mathcal{I}$`, `$\mathcal{E}$` (komenda `\mathcal{}`)
* **Przestrzenie liczbowe (LaTeX):** `$\mathbb{R}^k$` (komenda `\mathbb{}`)
* **Zastosowanie:** Zbiór wszystkich użytkowników (kaligrafia), zbiór wszystkich filmów, $k$-wymiarowa przestrzeń liczb rzeczywistych.

---
**Pamiętaj:** Kiedy definiujesz wektor $\mathbf{p}_u \in \mathbb{R}^k$, stosujesz notację pogrubioną. Kiedy jednak z tego wektora używasz konkretnej wartości z konkretnego $f$-tego wymiaru podczas dodawania we wzorze, używasz skalara: $p_{uf}$.
