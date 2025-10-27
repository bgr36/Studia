import random

# Stałe
DLUGOSC = 15
STACJE = {'A': 0, 'B': 7, 'C': 14}
SYGNAL_DL = 3
JAM_DL = 3

class Stacja:
    def __init__(self, nazwa, pozycja):
        self.nazwa = nazwa
        self.pozycja = pozycja
        self.czas_startu = random.randint(0, 5)
        self.nadaje = False
        self.jamuj = False
        self.kierunki = []  # 'L', 'P'
        self.krok_nadawania = 0
        self.krok_jamu = 0
        self.docelowa = None
        self.odbior_krok = 0  # Liczba pochłoniętych fragmentów

    def gotowa_do_nadawania(self, medium):
        lewo_ok = (self.pozycja - 1 >= 0 and medium[self.pozycja - 1] == '_')
        prawo_ok = (self.pozycja + 1 < len(medium) and medium[self.pozycja + 1] == '_')
        return lewo_ok and prawo_ok

    def rozpocznij_nadawanie(self):
        self.nadaje = True
        self.kierunki = ['L', 'P']
        self.krok_nadawania = 0
        self.docelowa = random.choice([k for k in STACJE if k != self.nazwa])
        print(f"Stacja {self.nazwa} rozpoczyna nadawanie do {self.docelowa}")

    def rozpocznij_jam(self):
        if not self.jamuj:
            print(f"Stacja {self.nazwa} wykryła kolizję i wysyła jam signal")
        self.nadaje = False
        self.jamuj = True
        self.krok_jamu = 0
        self.kierunki = ['L', 'P']

def przeslij_sygnaly(stacje, medium):
    aktywne_sygnaly = []
    kolidujace_stacje = set()

    for st in stacje:
        if st.nadaje:
            kolizja = False
            tymczasowe = []

            for d in range(1, SYGNAL_DL + 1):
                for kierunek in st.kierunki:
                    pos = st.pozycja - d if kierunek == 'L' else st.pozycja + d
                    if 0 <= pos < DLUGOSC:
                        if medium[pos] not in ['_', st.nazwa.lower()]:
                            kolizja = True
                        tymczasowe.append((pos, st.nazwa.lower()))

            if kolizja:
                for pos, _ in tymczasowe:
                    aktywne_sygnaly.append((pos, 'X'))
                kolidujace_stacje.add(st)
            else:
                aktywne_sygnaly.extend(tymczasowe)

        elif st.jamuj:
            for d in range(1, JAM_DL + 1):
                for kierunek in st.kierunki:
                    pos = st.pozycja - d if kierunek == 'L' else st.pozycja + d
                    if 0 <= pos < DLUGOSC:
                        aktywne_sygnaly.append((pos, 'J'))

    return aktywne_sygnaly, kolidujace_stacje

def aktualizuj_medium(medium, stacje, aktywne_sygnaly):
    nowe = ['_'] * DLUGOSC
    warstwy = [[] for _ in range(DLUGOSC)]

    for i, (pos, symbol) in enumerate(aktywne_sygnaly):
        warstwy[pos].append(symbol)

    for i in range(DLUGOSC):
        if 'J' in warstwy[i]:
            nowe[i] = 'J'
        elif len(warstwy[i]) == 0:
            nowe[i] = '_' if i not in STACJE.values() else medium[i]
        elif len(set(warstwy[i])) == 1:
            nowe[i] = warstwy[i][0]
        else:
            nowe[i] = 'X'

    # Umieść stacje
    for st in STACJE:
        nowe[STACJE[st]] = st

    return nowe

def sprawdz_odbior(medium, stacje):
    for st in stacje:
        if st.nadaje:
            pos_doc = STACJE[st.docelowa]
            segment = st.nazwa.lower()

            if medium[pos_doc] == segment:
                st.odbior_krok += 1
                medium[pos_doc] = '_'  # Wchłonięcie jednego segmentu
                if st.odbior_krok == SYGNAL_DL:
                    st.nadaje = False
                    st.odbior_krok = 0
                    print(f"Stacja {st.docelowa} zakończyła odbiór sygnału od {st.nazwa}")
    return

def wykonaj_ture(medium, stacje, tura):
    print(f"{tura:>2}. {''.join(medium)}")

    for st in stacje:
        if not st.nadaje and not st.jamuj and tura == st.czas_startu:
            if st.gotowa_do_nadawania(medium):
                st.rozpocznij_nadawanie()

    aktywne_sygnaly, kolidujace = przeslij_sygnaly(stacje, medium)

    for st in kolidujace:
        st.rozpocznij_jam()

    nowe_medium = aktualizuj_medium(medium, stacje, aktywne_sygnaly)

    sprawdz_odbior(nowe_medium, stacje)

    for st in stacje:
        if st.jamuj:
            st.krok_jamu += 1
            if st.krok_jamu >= JAM_DL:
                st.jamuj = False
        elif st.nadaje:
            st.krok_nadawania += 1
            if st.krok_nadawania >= 100:
                st.nadaje = False  # awaryjne zakończenie

    return nowe_medium

def symuluj(n_tur=20):
    stacje = [Stacja(nazwa, pos) for nazwa, pos in STACJE.items()]
    medium = ['_'] * DLUGOSC

    for st in STACJE:
        medium[STACJE[st]] = st

    for t in range(n_tur):
        medium = wykonaj_ture(medium, stacje, t)

if __name__ == "__main__":
    random.seed(2)  # powtarzalność
    symuluj(20)
