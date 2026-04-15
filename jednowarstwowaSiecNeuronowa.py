import os
import random
import math


ALFABET = "abcdefghijklmnopqrstuvwxyz"
ROZMIAR_ALFABETU = 26


def tekst_na_wektor_czestosci(tekst):
    """
    Zamienia tekst na wektor częstości liter a-z.
    Zwraca listę 26 liczb z zakresu [0, 1].
    """
    tekst = tekst.lower()
    liczniki = [0] * ROZMIAR_ALFABETU
    liczba_wszystkich_liter = 0

    for znak in tekst:
        if 'a' <= znak <= 'z':
            indeks = ord(znak) - ord('a')
            liczniki[indeks] += 1
            liczba_wszystkich_liter += 1

    if liczba_wszystkich_liter == 0:
        return [0.0] * ROZMIAR_ALFABETU

    return [licznik / liczba_wszystkich_liter for licznik in liczniki]


def wczytaj_plik(sciezka_pliku):
    """
    Wczytuje cały plik tekstowy jako string.
    """
    with open(sciezka_pliku, "r", encoding="utf-8") as plik:
        return plik.read()


def wczytaj_zbior_danych(sciezka_bazowa):
    sciezka_treningowa = os.path.join(sciezka_bazowa, "train")
    sciezka_testowa = os.path.join(sciezka_bazowa, "test")

    if not os.path.isdir(sciezka_treningowa):
        raise ValueError(f"Brak katalogu treningowego: {sciezka_treningowa}")
    if not os.path.isdir(sciezka_testowa):
        raise ValueError(f"Brak katalogu testowego: {sciezka_testowa}")

    jezyki = sorted([
        nazwa for nazwa in os.listdir(sciezka_treningowa)
        if os.path.isdir(os.path.join(sciezka_treningowa, nazwa))
    ])

    if len(jezyki) < 4:
        raise ValueError("Muszą być co najmniej 4 języki.")

    dane_treningowe = []
    dane_testowe = []

    for jezyk in jezyki:
        katalog = os.path.join(sciezka_treningowa, jezyk)
        pliki = [
            p for p in os.listdir(katalog)
            if os.path.isfile(os.path.join(katalog, p)) and p.endswith(".txt")
        ]

        for plik in pliki:
            sciezka = os.path.join(katalog, plik)
            tekst = wczytaj_plik(sciezka)
            wektor = tekst_na_wektor_czestosci(tekst)
            dane_treningowe.append((wektor, jezyk))

    for jezyk in jezyki:
        katalog = os.path.join(sciezka_testowa, jezyk)
        if not os.path.isdir(katalog):
            continue

        pliki = [
            p for p in os.listdir(katalog)
            if os.path.isfile(os.path.join(katalog, p)) and p.endswith(".txt")
        ]

        for plik in pliki:
            sciezka = os.path.join(katalog, plik)
            tekst = wczytaj_plik(sciezka)
            wektor = tekst_na_wektor_czestosci(tekst)
            dane_testowe.append((wektor, jezyk, plik))

    return dane_treningowe, dane_testowe, jezyki


class JednowarstwowaSiecNeuronowa:

    def __init__(self, rozmiar_wejscia, jezyki, wspolczynnik_uczenia=0.1):
        self.rozmiar_wejscia = rozmiar_wejscia
        self.jezyki = jezyki
        self.rozmiar_wyjscia = len(jezyki)
        self.wspolczynnik_uczenia = wspolczynnik_uczenia

        self.wagi = []
        self.biasy = []

        for _ in range(self.rozmiar_wyjscia):
            wagi = [random.uniform(-0.1, 0.1) for _ in range(rozmiar_wejscia)]
            bias = random.uniform(-0.1, 0.1)
            self.wagi.append(wagi)
            self.biasy.append(bias)

    def suma_wazona(self, x, neuron):
        suma = self.biasy[neuron]
        for i in range(self.rozmiar_wejscia):
            suma += self.wagi[neuron][i] * x[i]
        return suma

    def softmax(self, wyniki):
        maksimum = max(wyniki)
        exp_wyniki = [math.exp(w - maksimum) for w in wyniki]
        suma = sum(exp_wyniki)
        return [w / suma for w in exp_wyniki]

    def przewidz_z_prawdopodobienstwami(self, x):
        wyniki = [self.suma_wazona(x, i) for i in range(self.rozmiar_wyjscia)]
        prawdopodobienstwa = self.softmax(wyniki)

        ranking = list(zip(self.jezyki, prawdopodobienstwa))
        ranking.sort(key=lambda para: para[1], reverse=True)
        return ranking

    def przewidz(self, x):
        ranking = self.przewidz_z_prawdopodobienstwami(x)
        return ranking[0][0]

    def ucz(self, dane_treningowe, liczba_epok=100):
        for epoka in range(liczba_epok):
            random.shuffle(dane_treningowe)
            liczba_bledow_w_epoce = 0

            for x, prawdziwy_jezyk in dane_treningowe:
                for j, jezyk in enumerate(self.jezyki):

                    target = 1 if jezyk == prawdziwy_jezyk else 0

                    net = self.suma_wazona(x, j)
                    output = 1 if net >= 0 else 0

                    blad = target - output

                    if blad != 0:
                        liczba_bledow_w_epoce += 1

                        for i in range(self.rozmiar_wejscia):
                            self.wagi[j][i] += self.wspolczynnik_uczenia * blad * x[i]

                        self.biasy[j] += self.wspolczynnik_uczenia * blad

            print(f"Epoka {epoka+1}/{liczba_epok} - błędy: {liczba_bledow_w_epoce}")

    def testuj(self, dane_testowe):
        poprawne = 0

        print("\nWYNIKI:")
        print("-" * 60)

        for x, prawdziwy, nazwa in dane_testowe:
            ranking = self.przewidz_z_prawdopodobienstwami(x)
            przewidziany = ranking[0][0]

            print(f"\nPlik: {nazwa}")
            print(f"Poprawny język: {prawdziwy}")
            print(f"Przewidziany język: {przewidziany}")
            print("Prawdopodobieństwa:")

            for jezyk, prawd in ranking:
                print(f"  - {jezyk}: {prawd:.2%}")

            if przewidziany == prawdziwy:
                poprawne += 1

        skutecznosc = poprawne / len(dane_testowe)
        print(f"\nSkuteczność: {skutecznosc:.2%}")


def tekst_recznie(siec):
    print("\nWpisz tekst:")
    tekst = input()
    wektor = tekst_na_wektor_czestosci(tekst)

    ranking = siec.przewidz_z_prawdopodobienstwami(wektor)

    print("\nKlasyfikacja:")
    print(f"Najbardziej prawdopodobny język: {ranking[0][0]}")
    print("Prawdopodobieństwa:")

    for jezyk, prawd in ranking:
        print(f"  - {jezyk}: {prawd:.2%}")


def plik_test(siec):
    sciezka = input("Podaj ścieżkę: ")

    try:
        tekst = wczytaj_plik(sciezka)
    except FileNotFoundError:
        print("Błąd: nie znaleziono pliku.")
        return
    except Exception as e:
        print(f"Błąd podczas wczytywania pliku: {e}")
        return

    wektor = tekst_na_wektor_czestosci(tekst)
    ranking = siec.przewidz_z_prawdopodobienstwami(wektor)

    print("\nKlasyfikacja:")
    print(f"Najbardziej prawdopodobny język: {ranking[0][0]}")
    print("Prawdopodobieństwa:")

    for jezyk, prawd in ranking:
        print(f"  - {jezyk}: {prawd:.2%}")


def main():
    sciezka = input("Podaj folder z danymi: ")

    dane_treningowe, dane_testowe, jezyki = wczytaj_zbior_danych(sciezka)

    print("Języki:", jezyki)

    siec = JednowarstwowaSiecNeuronowa(26, jezyki)

    siec.ucz(dane_treningowe, 100)
    siec.testuj(dane_testowe)

    while True:
        print("\n1 - tekst")
        print("2 - plik")
        print("3 - koniec")

        wybor = input()

        if wybor == "1":
            tekst_recznie(siec)
        elif wybor == "2":
            plik_test(siec)
        else:
            break


if __name__ == "__main__":
    main()

