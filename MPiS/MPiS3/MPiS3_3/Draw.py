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

# Funkcja do tworzenia wykresów punktowych ze średnimi
def plot_results(n_values, results, averages, title, filename):
    plt.figure(figsize=(12, 6))
    
    # Rysujemy wyniki poszczególnych testów jako punkty
    for result in results:
        plt.scatter(n_values, result, alpha=0.5, color='blue', label='Wyniki testów' if result is results[0] else "")
    
    # Rysujemy średnią jako większy, wyróżniony punkt
    plt.scatter(n_values, averages, color='red', s=100, label='Średnia', zorder=5, edgecolor='black')
    
    # Ustawienia wykresu
    plt.xlabel("n")
    plt.ylabel("Liczba rund T(n)")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.show()

# Główna funkcja
def main():
    # Ścieżka do katalogu z plikami
    os.chdir("C:/Users/janke/Desktop/MPiS3/MPiS3_3")
    print(f"Nowy katalog roboczy: {os.getcwd()}")
    
    files = {
        "Test01_results.csv": "Liczba rund T(n) dla p = 0.1",
        "Test05_results.csv": "Liczba rund T(n) dla p = 0.5"
    }
    
    for filename, title in files.items():
        if os.path.exists(filename):
            print(f"Przetwarzam plik: {filename}")
            n_values, results, averages = load_csv(filename)
            plot_results(n_values, results, averages, title, filename.replace(".csv", "_scatter.png"))

                        # (b) Wykres średnich ilorazów cmp(n)/n lub s(n)/n
            plot_ratios(
                n_values,
                averages,
                denominator_func=lambda x: x,
                title=f"{title} / n od n",
                ylabel=f"{title} / n",
                filename=filename.replace(".csv", "_ratio_n.png")
            )
            
            # (c) Wykres średnich ilorazów cmp(n)/n^2 lub s(n)/n^2
            plot_ratios(
                n_values,
                averages,
                denominator_func=lambda x: np.array(x)**2,
                title=f"{title} / n² od n",
                ylabel=f"{title} / n²",
                filename=filename.replace(".csv", "_ratio_n2.png")
            )

        else:
            print(f"Plik {filename} nie istnieje!")

if __name__ == "__main__":
    main()
