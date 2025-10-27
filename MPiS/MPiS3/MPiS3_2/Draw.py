import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Funkcja do wczytywania plików CSV
def load_csv(filename):
    df = pd.read_csv(filename)
    n_values = [int(col) for col in df.columns[1:-1]]  # Pobieramy wartości n (kolumny)
    results = df.iloc[:-1, 1:-1].values                # Pobieramy wyniki testów
    averages = df.iloc[-1, 1:-1].values.astype(float)  # Pobieramy średnie
    return n_values, results, averages

# Funkcja do rysowania wykresów ilorazów
def plot_ratios(n_values, averages, denominator_func, title, ylabel, filename):
    ratios = averages / denominator_func(n_values)  # Wyliczamy iloraz
    plt.figure(figsize=(12, 6))
    plt.plot(n_values, ratios, marker='o', color='green', linewidth=2, label=ylabel)
    plt.xlabel("n")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.show()

# Funkcja do rysowania wykresu cmp(n) lub s(n)
def plot_averages(n_values, averages, title, ylabel, filename):
    plt.figure(figsize=(12, 6))
    plt.plot(n_values, averages, marker='o', color='blue', linewidth=2, label=ylabel)
    plt.xlabel("n")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.show()

# Główna funkcja
def main():
    # Ścieżka do katalogu z plikami
    os.chdir("C:/Users/janke/Desktop/MPiS3/MPiS3_2")  # Dostosuj ścieżkę do swoich plików
    print(f"Nowy katalog roboczy: {os.getcwd()}")
    
    files = {
        "Comparisons_results.csv": "Liczba porównań",
        "Swaps_results.csv": "Liczba przestawień"
    }
    
    for filename, ylabel_base in files.items():
        if os.path.exists(filename):
            print(f"Przetwarzam plik: {filename}")
            n_values, results, averages = load_csv(filename)
            
            # (a) Wykres średnich cmp(n) lub s(n)
            plot_averages(
                n_values,
                averages,
                title=f"{ylabel_base} od n",
                ylabel=f"{ylabel_base}",
                filename=filename.replace(".csv", "_averages.png")
            )
            
            # (b) Wykres średnich ilorazów cmp(n)/n lub s(n)/n
            plot_ratios(
                n_values,
                averages,
                denominator_func=lambda x: x,
                title=f"{ylabel_base} / n od n",
                ylabel=f"{ylabel_base} / n",
                filename=filename.replace(".csv", "_ratio_n.png")
            )
            
            # (c) Wykres średnich ilorazów cmp(n)/n^2 lub s(n)/n^2
            plot_ratios(
                n_values,
                averages,
                denominator_func=lambda x: np.array(x)**2,
                title=f"{ylabel_base} / n² od n",
                ylabel=f"{ylabel_base} / n²",
                filename=filename.replace(".csv", "_ratio_n2.png")
            )
        else:
            print(f"Plik {filename} nie istnieje!")

if __name__ == "__main__":
    main()
