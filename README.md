# 🧠 Jednowarstwowa sieć neuronowa do klasyfikacji języka

Projekt przedstawia implementację jednowarstwowej sieci neuronowej w Pythonie, służącej do klasyfikacji tekstów według języka. Model został zaimplementowany od podstaw, bez użycia zewnętrznych bibliotek do uczenia maszynowego.

## 🎯 Opis projektu

Program analizuje tekst i na podstawie częstości występowania liter określa język, w jakim został napisany. Każdy tekst zamieniany jest na wektor cech o długości 26 (litery alfabetu), który następnie przetwarzany jest przez sieć neuronową. Każdy neuron odpowiada jednemu językowi.

## ✨ Funkcjonalności

- klasyfikacja języka tekstu  
- obsługa wielu języków (minimum 4)  
- trenowanie modelu na danych z plików tekstowych  
- testowanie na zbiorze testowym  
- ręczne wpisywanie tekstu do klasyfikacji  
- klasyfikacja plików `.txt`  
- zwracanie prawdopodobieństw dla wszystkich języków  
- obliczanie skuteczności modelu  

## ▶️ Uruchomienie

### Wymagania
- Python 3  

### Uruchomienie programu

```bash
python3 jednowarstwowaSiecNeuronowa.py
```

## 🧪 Testowanie

Program oferuje dwa tryby pracy:

- **Tekst** – użytkownik wpisuje własny tekst, który zostaje sklasyfikowany  
- **Plik** – użytkownik podaje ścieżkę do pliku `.txt`, np.:

```bash
test/english/test1.txt
```

## 📊 Wyniki
Program dla każdego testu zwraca:

- przewidziany język
- prawdopodobieństwa dla wszystkich języków
- skuteczność dla danych testowych

## ⚠️ Ograniczenia
Model opiera się wyłącznie na analizie częstości liter, dlatego najlepiej działa dla dłuższych tekstów. Krótkie słowa mogą być klasyfikowane mniej dokładnie.

## 🛠️ Technologie
- Python
- programowanie obiektowe
- przetwarzanie tekstu
- podstawy uczenia maszynowego (implementacja od podstaw)
