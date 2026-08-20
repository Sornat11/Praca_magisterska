# Ściągawka: Interpretacja Metryk (Implicit Feedback / VOD)

W systemach rekomendacyjnych opartych na zbiorach dorozumianych (*implicit feedback*), takich jak MovieLens-1M w zadaniu Top-N rekomendacji (najczęściej mierzy się **Top-10** lub **Top-20**), metryki przyjmują znacznie niższe, "bardziej brutalne" wartości niż w zadaniach klasyfikacji (gdzie Accuracy na poziomie 90% to standard).

Złożoność problemu (6000 użytkowników i prawie 4000 filmów) sprawia, że trafienie jakiegokolwiek filmu z puli testowej na liście zaledwie 10 rekomendacji to ogromne wyzwanie obliczeniowe.

Poniżej znajduje się orientacyjna interpretacja najpopularniejszych metryk dla list **Top-10**, która pomoże Ci ocenić swoje eksperymenty (odnosi się to do standardowego podziału zbioru ML-1M, np. Leave-One-Out lub 80/20):

## 1. Recall@10 (Czułość)
**Mówi nam:** *Jaki procent ze wszystkich filmów, które użytkownik naprawdę później obejrzał (zbioru testowego), udało się nam zamknąć w zaledwie 10 kafelkach naszej rekomendacji?*
* **Poniżej 0.05 (5%)** – Bardzo słabo. Model jest w dużej mierze losowy.
* **0.05 – 0.12 (5% - 12%)** – Przeciętnie. Wynik uzyskiwany przez najprostsze metody baseline (np. naiwne liczenie popularności).
* **0.15 – 0.22 (15% - 22%)** – Solidnie / Dobrze. Takie wyniki osiągają silne modele CF z optymalizacją parową (jak Twój BPR-MF).
* **Powyżej 0.25 (25%)** – Znakomicie! Algorytmy klasy NCF (Neural Collaborative Filtering) lub LightGCN oscylują w okolicach tego pułapu. 

## 2. NDCG@10 (Znormalizowana zdyskontowana zyskowność skumulowana)
**Mówi nam:** *Czy trafne polecenia umieściliśmy na samym szczycie listy (miejsca 1, 2, 3), czy zakopaliśmy je na samym dole (miejsca 8, 9, 10)? NDCG surowo karze za dawanie trafień nisko.*
* **Poniżej 0.10** – Słabo. Trafiamy w gusta rzadko, a jak już, to na samym dole listy.
* **0.15 – 0.25** – Wynik poprawny, oczekiwany przy klasycznych k-najbliższych sąsiadach (ItemKNN).
* **0.30 – 0.40** – Wynik doskonały! Osiągany przy bardzo precyzyjnych modelach (LightGCN, optymalizowane parametry). Z reguły w badaniach naukowych na ML-1M walka toczy się właśnie o przebicie bariery 0.40 dla NDCG@10.

## 3. Precision@10 (Precyzja)
**Mówi nam:** *Ile spośród poleconych 10 filmów okazało się strzałem w dziesiątkę dla tego konkretnego użytkownika?*
*Wskazówka: Precyzja w rekomendacjach jest naturalnie niska, bo użytkownik w zbiorze testowym ma np. tylko 5 ukrytych filmów do odgadnięcia, a Ty dajesz mu 10. Max wynik wynosiłby wtedy i tak 0.5.*
* **0.00 – 0.10** – Słabo. Tylko mniej niż 1 na 10 rekomendacji ma sens.
* **0.15 – 0.25** – Bardzo dobry standard. Przeciętnie odgadujemy 2-3 z 10 kafelków na stronie głównej VOD, co użytkownik odbiera jako silnie "dopasowaną do niego" ofertę.

## 4. MRR (Średnia odwrotność rangi)
**Mówi nam:** *Jak wysoko w naszym rankingu znalazła się pierwsza, celna rekomendacja?* 
* MRR = 1.0 $\rightarrow$ pierwszy kafel to strzał w dziesiątkę (1/1).
* MRR = 0.5 $\rightarrow$ na drugim miejscu jest pierwszy strzał (1/2).
* MRR = 0.33 $\rightarrow$ na trzecim (1/3).
* **Wniosek:** Średnie MRR całego modelu na poziomie ok. **0.40 - 0.55** to fenomenalny wynik i świadczy o wybitnej zdolności rankującej BPR, natomiast wartość **0.10 - 0.20** oznacza, że Twój algorytm wypycha celne strzały gdzieś za horyzont przeglądarki.

## 5. Hit Rate (HR@10)
**Mówi nam:** *Z jakim prawdopodobieństwem w ogóle udało nam się dostarczyć użytkownikowi chociaż jedną dobrą rekomendację? (Czy użytkownik natrafił w Top-10 na cokolwiek pozytywnego?)* W przeciwieństwie do Recall (który wskazuje na jaki odsetek ze wszystkich celów zapolowaliśmy), HR to brutalna statystyka binarna na użytkownika: 1 jeśli w Top-10 było przynajmniej 1 trafienie, 0 jeśli nie było niczego trafnego.
*Uwaga badawcza: Jeżeli w swojej pracy wdrożysz dla RecBole procedurę testową typu "Leave-One-Out" (ukrywanie wyłącznie jednego, ostatniego filmu z osi czasu w teście), wartość metryki Hit Rate zrówna się matematycznie co do joty z wynikiem metryki Recall, ponieważ mianownik ułamka dla każdego użytkownika wynosi dokładnie 1. W przypadku standardowego podziału 80/20, wartości kształtują się następująco:*
* **Poniżej 0.20** – Słaby biznesowo wynik. Oznacza, że aż dla 80% logujących się widzów generujemy pustą, nieużyteczną stronę bez żadnego trafienia.
* **0.30 – 0.50** – Solidny, książkowy standard (typowe wyniki na MovieLens-1M). Osiągamy gwarantowane zainteresowanie chociaż jednym kafelkiem u 3 do 5 widzów na każdą dziesiątkę.
* **Powyżej 0.60** – Fenomenalnie. Ponad połowa naszej bazy widzi zawsze minimum jedną trafioną pozycję zaraz po załadowaniu głównej witryny VOD. Nowoczesne GNN pomagają wypychać tę wartość właśnie do takich progów.

---
**Pamiętaj:** Kiedy wykonasz w RecBole fazę ewaluacji na swoich modelach, nie dziw się, jeśli NDCG czy Recall wyniosą ułamki dziesiętne takie jak "0.1932". W świecie uczenia maszynowego nad grafami to właśnie jest twardy, naukowy dowód skuteczności!
