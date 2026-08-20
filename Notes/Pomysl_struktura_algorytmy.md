# Pomysł na przyszłą strukturę rozdziału o algorytmach
*(Zapisano podczas dyskusji o przebudowie 30_second_chapter.tex)*

## Założenie
Zamiast dzielić algorytmy na szerokie kategorie ("Filtrowanie kolaboracyjne", "Uczenie głębokie", "Grafy"), układamy je w **ciąg ewolucyjny**. Każdy kolejny podrozdział wprowadza model, który rozwiązuje konkretną wadę modelu poprzedniego.

## Proponowana struktura (kod LaTeX)

```latex
\subsection{Architektury badanych algorytmów rekomendacyjnych}

\subsubsection{Algorytm oparty na sąsiedztwie: ItemKNN}
% Wada na koniec: Nie radzi sobie z ekstremalnie rzadkimi danymi.

\subsubsection{Modele czynników ukrytych: Faktoryzacja Macierzy (MF)}
% Rozwiązanie: Rzutowanie do gęstej przestrzeni wektorowej. 
% Wada na koniec: Standardowo używa błędu punktowego (MSE).

\subsubsection{Optymalizacja rankingu: BPR-MF}
% Rozwiązanie: Funkcja straty ucząca się poprawnego sortowania (błąd parowy).
% Wada na koniec: Iloczyn skalarny wymusza tylko liniowe modelowanie relacji.

\subsubsection{Podejście neuronowe: Neural Matrix Factorization (NeuMF)}
% Rozwiązanie: Zastąpienie iloczynu skalarnego wielowarstwową siecią neuronową (MLP) w celu modelowania nieliniowego.
% Wada na koniec: Model ignoruje szerszy kontekst społeczny/strukturalny bazy danych.

\subsubsection{Podejście grafowe: LightGCN}
% Rozwiązanie: Wygładzanie wektorów cech po grafie interakcji przed ostatecznym obliczeniem predykcji.
```

## Dlaczego warto?
Taki układ buduje spójną narrację naukową, wykazując głębokie zrozumienie tematu. Pokazuje, jak poszczególne algorytmy nie są ze sobą luźno powiązane, lecz wynikają z historycznej potrzeby optymalizacji i pokonywania kolejnych barier architektonicznych.
