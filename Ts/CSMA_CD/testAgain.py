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
        self.docelowa = None  # Losowana później
        self.odbior_krok = 0  # Ile segmentów już wchłonięto

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
        self.nadaje = False
        self.jamuj = True
        self.krok_jamu = 0
        self.kierunki = ['L', 'P']
        print(f"Stacja {self.nazwa} wykryła kolizję i wysyła jam signal")

def aktualizuj_medium(medium, stacje, aktywne_sygnaly):
    nowe = ['_'] * DLUGOSC

    # Umieść stacje
    for st in STACJE:
        nowe[STACJE[st]] = st

    # Rozmieść sygnały
    warstwy = [[] for _ in range(DLUGOSC)]
    for i, (indeks, symbol) in enumerate(aktywne_sygnaly):
        warstwy[indeks].append(symbol)

    for i in range(DLUGOSC):
        if len(warstwy[i]) == 0:
            continue
        elif 'J' in warstwy[i]:
            nowe[i] = 'J'
        elif len(set(warstwy[i])) == 1:
            nowe[i] = warstwy[i][0]
        else:
            nowe[i] = 'X'

    return nowe

def przeslij_sygnaly(stacje, medium):
    aktywne_sygnaly = []

    for st in stacje:
        pozycja = st.pozycja
        if st.nadaje:
            for d in range(SYGNAL_DL):
                if 'L' in st.kierunki and pozycja - (d + 1) >= 0:
                    aktywne_sygnaly.append((pozycja - (d + 1), st.nazwa.lower()))
                if 'P' in st.kierunki and pozycja + (d + 1) < DLUGOSC:
                    aktywne_sygnaly.append((pozycja + (d + 1), st.nazwa.lower()))
        elif st.jamuj:
            for d in range(JAM_DL):
                if 'L' in st.kierunki and pozycja - (d + 1) >= 0:
                    aktywne_sygnaly.append((pozycja - (d + 1), 'J'))
                if 'P' in st.kierunki and pozycja + (d + 1) < DLUGOSC:
                    aktywne_sygnaly.append((pozycja + (d + 1), 'J'))
    return aktywne_sygnaly

def wykryj_kolizje(medium, stacje):
    for st in stacje:
        for d in range(1, SYGNAL_DL + 1):
            for kierunek in ['L', 'P']:
                pos = st.pozycja - d if kierunek == 'L' else st.pozycja + d
                if 0 <= pos < DLUGOSC and medium[pos] == 'X':
                    st.rozpocznij_jam()
                    break

def sprawdz_odbior(medium, stacje):
    for st in stacje:
        if st.nadaje:
            pos_doc = STACJE[st.docelowa]
            segment = st.nazwa.lower()
            if all(
                medium[pos_doc - d] == segment
                for d in range(SYGNAL_DL)
                if 0 <= pos_doc - d < DLUGOSC
            ):
                st.nadaje = False
                st.odbior_krok = 0
                print(f"Stacja {st.docelowa} odbiera sygnał od {st.nazwa}")
                return (st, pos_doc, segment)
    return None

def wykonaj_ture(medium, stacje, tura):
    print(f"{tura:>2}. {''.join(medium)}")

    for st in stacje:
        if not st.nadaje and not st.jamuj and tura == st.czas_startu:
            if st.gotowa_do_nadawania(medium):
                st.rozpocznij_nadawanie()

    aktywne_sygnaly = przeslij_sygnaly(stacje, medium)
    nowe_medium = aktualizuj_medium(medium, stacje, aktywne_sygnaly)

    wykryj_kolizje(nowe_medium, stacje)

    odebrane = sprawdz_odbior(nowe_medium, stacje)
    if odebrane:
        st, pos, znak = odebrane
        for i in range(SYGNAL_DL):
            if pos - i >= 0 and nowe_medium[pos - i] == znak:
                nowe_medium[pos - i] = '_'

    for st in stacje:
        if st.jamuj:
            st.krok_jamu += 1
            if st.krok_jamu >= JAM_DL:
                st.jamuj = False
        elif st.nadaje:
            st.krok_nadawania += 1
            if st.krok_nadawania >= SYGNAL_DL:
                st.nadaje = False

    return nowe_medium

# 🔁 Symulacja
def symuluj(n_tur=20):
    stacje = [Stacja(nazwa, pos) for nazwa, pos in STACJE.items()]
    medium = ['_'] * DLUGOSC

    for st in STACJE:
        medium[STACJE[st]] = st

    for t in range(n_tur):
        medium = wykonaj_ture(medium, stacje, t)

# ▶️ Uruchom
if __name__ == "__main__":
    random.seed(2)  # dla powtarzalnych wyników
    symuluj(20)
