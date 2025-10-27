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

# Funkcja do rysowania wykresów dla danych z TestA i TestB
def plot_special_ratios(n_values, averages, func, title, ylabel, filename):
    transformed_ratios = averages / func(n_values)  # Wyliczamy specjalny iloraz
    plt.figure(figsize=(12, 6))
    plt.plot(n_values, transformed_ratios, marker='o', color='purple', linewidth=2, label=ylabel)
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
    os.chdir("C:/Users/janke/Desktop/MPiS3/MPiS3_1")  # Dostosuj ścieżkę do swoich plików
    print(f"Nowy katalog roboczy: {os.getcwd()}")
    
    # Dodatkowe pliki z transformacjami matematycznymi
    special_files = {
        "TestA_results.csv": {
            "title": "Średnie TestA / (ln(n) / ln(ln(n)))",
            "ylabel": "Średnie TestA / (ln(n) / ln(ln(n)))",
            "func": lambda n: np.log(n) / np.log(np.log(n))
        },
        "TestB_results.csv": {
            "title": "Średnie TestB / (ln(ln(n)) / ln(2))",
            "ylabel": "Średnie TestB / (ln(ln(n)) / ln(2))",
            "func": lambda n: np.log(np.log(n)) / np.log(2)
        }
    }
    
    for filename, params in special_files.items():
        if os.path.exists(filename):
            print(f"Przetwarzam plik: {filename}")
            n_values, _, averages = load_csv(filename)
            
            # Tworzenie wykresu specjalnych ilorazów
            plot_special_ratios(
                n_values,
                averages,
                func=params["func"],
                title=params["title"],
                ylabel=params["ylabel"],
                filename=filename.replace(".csv", "_special_ratio.png")
            )
        else:
            print(f"Plik {filename} nie istnieje!")

if __name__ == "__main__":
    main()
