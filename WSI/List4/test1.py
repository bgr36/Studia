import numpy as np
import matplotlib.pyplot as plt

# Spróbuj zaimportować torchvision, jeśli jest dostępny.
# Jeśli nie masz PyTorch, kod wyświetli ostrzeżenie.
try:
    import torchvision.datasets as datasets
    import torchvision.transforms as transforms
except ImportError:
    print("Ostrzeżenie: Biblioteka 'torchvision' nie znaleziona. ")
    print("Proszę zainstalować PyTorch i torchvision (pip install torch torchvision) ")
    print("lub dostosować kod do ręcznego wczytywania danych EMNIST.")
    datasets = None

# Spróbuj zaimportować seaborn dla ładniejszych heatmap.
# Jeśli nie masz seaborn, wykresy będą prostsze.
try:
    import seaborn as sns
except ImportError:
    print("Ostrzeżenie: Biblioteka 'seaborn' nie znaleziona. Wykresy heatmap mogą być prostsze.")
    sns = None

# --- Funkcja do wczytywania i przygotowania danych EMNIST ---
def load_emnist_data():
    """
    Wczytuje dane treningowe EMNIST (podzbiór 'digits') za pomocą torchvision.
    Spłaszcza obrazy do wektorów 1D i normalizuje wartości pikseli.
    """
    X = None
    y = None

    if datasets is not None:
        print("\n--- Wczytywanie danych EMNIST (digits) ---")
        print("Pobieranie i przygotowywanie danych, może to chwilę potrwać...")
        # emnist_train zawiera tylko cyfry 0-9, co odpowiada MNISTowi.
        emnist_train = datasets.EMNIST(root='./data', split='digits', train=True, download=True,
                                       transform=transforms.ToTensor())

        X_list = []
        y_list = []
        for i, (img, label) in enumerate(emnist_train):
            X_list.append(img.numpy().flatten()) # Spłaszcz obraz 28x28 do wektora 784
            y_list.append(label)
            if (i + 1) % 10000 == 0: # Informacja o postępie co 10 000 próbek
                print(f"  Przygotowano {i + 1} próbek...")

        X = np.array(X_list).astype(float) # Upewnij się, że dane są typu float
        y = np.array(y_list)

        print(f"Zakończono wczytywanie. Wczytano łącznie {len(X)} próbek EMNIST (cyfry).")
    else:
        print("Błąd: Nie można wczytać danych EMNIST. 'torchvision' nie jest dostępny.")
        print("Proszę zainstalować PyTorch i torchvision, aby program działał poprawnie.")
        return None, None # Zwróć None, aby zasygnalizować błąd

    return X, y

# --- Klasa KMeansCustom: Samodzielna implementacja K-średnich ---
class KMeansCustom:
    def __init__(self, n_clusters, max_iter=300, n_init=10):
        """
        Inicjalizuje algorytm K-średnich.
        :param n_clusters: Liczba klastrów (K).
        :param max_iter: Maksymalna liczba iteracji w każdej próbie.
        :param n_init: Liczba prób inicjalizacji centroidów (dla wyboru najlepszej klasteryzacji).
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.n_init = n_init
        self.centroids = None
        self.labels = None
        self.inertia_ = float('inf') # Przechowuje najniższą inercję znalezioną we wszystkich próbach

    # Ta funkcja nie jest już używana w głównym cyklu, zastąpiona przez wektoryzowane obliczenia.
    # Zostawiona jako pomocnicza dla zrozumienia.
    def _euclidean_distance(self, point1, point2):
        """Oblicza odległość euklidesową między dwoma punktami."""
        return np.sqrt(np.sum((point1 - point2)**2))

    def _calculate_inertia(self, X, labels, centroids):
        """Oblicza inercję (sumę kwadratów odległości próbek do ich centroidów)."""
        inertia = 0
        for i in range(self.n_clusters):
            cluster_points = X[labels == i]
            if len(cluster_points) > 0: # Upewnij się, że klaster nie jest pusty
                inertia += np.sum(np.sum((cluster_points - centroids[i])**2, axis=1))
        return inertia

    def _initialize_centroids_kmeans_plusplus(self, X):
        """Inicjalizuje centroidy metodą k-means++ z wektoryzacją."""
        n_samples, n_features = X.shape
        centroids = np.zeros((self.n_clusters, n_features))

        # 1. Wybierz pierwszy centroid losowo spośród punktów danych
        first_centroid_idx = np.random.randint(0, n_samples)
        centroids[0] = X[first_centroid_idx]

        # 2. Dla pozostałych centroidów
        for i in range(1, self.n_clusters):
            # Oblicz kwadraty odległości wszystkich punktów do WSZYSTKICH JUŻ WYBRANYCH centroidów
            X_squared_sum = np.sum(X**2, axis=1, keepdims=True) # (N, 1)
            temp_centroids = centroids[0:i]
            temp_centroids_squared_sum = np.sum(temp_centroids**2, axis=1, keepdims=True).T # (1, i)

            dot_product = np.dot(X, temp_centroids.T) # (N, i)

            # distance_to_all_selected_centroids_sq: (N, i)
            distance_to_all_selected_centroids_sq = X_squared_sum + temp_centroids_squared_sum - 2 * dot_product

            # Znajdź minimalną odległość dla każdego punktu do najbliższego już wybranego centroidu
            distances_sq = np.min(distance_to_all_selected_centroids_sq, axis=1) # (N,)

            # !!! WAŻNA ZMIANA: Upewnij się, że wszystkie wartości są nieujemne !!!
            # Zastąp wszelkie wartości mniejsze od zera (np. -1e-10) zerem.
            distances_sq = np.maximum(distances_sq, 0)

            # Wybierz nowy centroid z prawdopodobieństwem proporcjonalnym do kwadratu odległości.
            sum_distances_sq = np.sum(distances_sq)
            if sum_distances_sq == 0:
                # Jeśli suma odległości jest zero (wszystkie punkty są tak samo blisko już wybranych centroidów
                # lub wszystkie są identyczne), wybierz nowy centroid równomiernie losowo.
                probabilities = np.ones(n_samples) / n_samples
            else:
                probabilities = distances_sq / sum_distances_sq

            new_centroid_idx = np.random.choice(n_samples, p=probabilities)
            centroids[i] = X[new_centroid_idx]
        return centroids

    def fit(self, X):
        """
        Dopasowuje algorytm K-średnich do danych X, wykonując `n_init` prób
        i wybierając najlepszą klasteryzację.
        """
        best_centroids = None
        best_labels = None
        best_inertia = float('inf')

        n_samples = X.shape[0]

        # Wykonaj wiele prób inicjalizacji, aby znaleźć klasteryzację o najmniejszej inercji
        for init_attempt in range(self.n_init):
            print(f"\n  Rozpoczynam próbę inicjalizacji {init_attempt + 1}/{self.n_init}...")
            print(f"  Inicjalizowanie centroidów metodą k-means++...")
            current_centroids = self._initialize_centroids_kmeans_plusplus(X)
            print(f"  Centroidy zainicjalizowane. Rozpoczynam iteracje...")

            current_labels = np.zeros(n_samples, dtype=int)

            # Główna pętla iteracyjna algorytmu K-średnich
            for iteration in range(self.max_iter):
                # Krok 1: Przypisanie każdego punktu do najbliższego centroidu (wektoryzacja)
                # Oblicz kwadraty odległości wszystkich punktów do WSZYSTKICH centroidów
                X_squared_sum = np.sum(X**2, axis=1, keepdims=True) # (N, 1)
                centroids_squared_sum = np.sum(current_centroids**2, axis=1, keepdims=True).T # (1, K)
                dot_product = np.dot(X, current_centroids.T) # (N, K)

                # distance_matrix_sq: (N, K) - macierz kwadratów odległości
                distance_matrix_sq = X_squared_sum + centroids_squared_sum - 2 * dot_product

                # new_labels: (N,) - etykiety przypisane do każdego punktu
                new_labels = np.argmin(distance_matrix_sq, axis=1)

                # Krok 2: Obliczanie nowych centroidów jako średniej z przypisanych punktów
                new_centroids = np.zeros_like(current_centroids)
                for i in range(self.n_clusters):
                    cluster_points = X[new_labels == i]
                    if len(cluster_points) > 0:
                        new_centroids[i] = np.mean(cluster_points, axis=0) # Oblicz średnią punktów w klastrze
                    else:
                        # Obsługa pustego klastra: zainicjuj centroid losowym punktem z danych,
                        # aby uniknąć błędów i spróbować "ożywić" klaster.
                        new_centroids[i] = X[np.random.randint(0, n_samples)]

                # Sprawdzenie zbieżności: jeśli centroidy już się nie zmieniają lub ich zmiana jest minimalna
                if np.allclose(new_centroids, current_centroids, atol=1e-6):
                    print(f"    Zbieżność osiągnięta w iteracji {iteration + 1}.")
                    break # Algorytm zbiegł, zakończ pętlę iteracji
                current_centroids = new_centroids
                current_labels = new_labels

                if (iteration + 1) % 50 == 0: # Drukuj postęp co 50 iteracji
                     print(f"    Iteracja {iteration + 1}/{self.max_iter} zakończona...")

            # Oblicz inercję dla bieżącej próby inicjalizacji
            # Możemy użyć distance_matrix_sq dla optymalizacji tutaj również
            current_inertia = np.sum(distance_matrix_sq[np.arange(n_samples), new_labels])
            print(f"  Zakończono próbę {init_attempt + 1}. Inercja: {current_inertia:.2f}")

            # Zaktualizuj najlepsze wyniki, jeśli bieżąca inercja jest niższa
            if current_inertia < best_inertia:
                best_inertia = current_inertia
                best_centroids = current_centroids
                best_labels = current_labels
                print(f"  Znaleziono lepszą klasteryzację! Nowa najlepsza inercja: {best_inertia:.2f}")

        self.centroids = best_centroids
        self.labels = best_labels
        self.inertia_ = best_inertia
        print("\nKlasteryzacja K-średnich zakończona. Wybrano klasteryzację o najniższej inercji.")

# --- Funkcje do wizualizacji wyników ---
def plot_centroids(centroids, title):
    """
    Wyświetla obrazy centroidów w siatce.
    Centroidy są wektorami 1D i są przekształcane z powrotem na obrazy 28x28.
    """
    num_centroids = len(centroids)
    # Oblicz optymalną siatkę wyświetlania dla lepszej czytelności
    n_cols = min(num_centroids, 10) # Maksymalnie 10 kolumn
    n_rows = (num_centroids + n_cols - 1) // n_cols # Oblicz wymaganą liczbę rzędów

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(2 * n_cols, 2 * n_rows))
    # Upewnij się, że 'axes' jest zawsze tablicą 1D, aby łatwo iterować
    axes = axes.flatten() if n_rows > 1 or n_cols > 1 else [axes]

    for i, centroid in enumerate(centroids):
        # Spłaszczony wektor 784 elementów jest przekształcany na obraz 28x28
        axes[i].imshow(centroid.reshape(28, 28), cmap='gray_r')
        axes[i].axis('off') # Usuń osie
        axes[i].set_title(f'C {i}') # Tytuł centroidu (np. C 0, C 1)

    # Wyłącz pozostałe puste sub-wykresy, jeśli jest ich mniej niż siatka
    for j in range(num_centroids, len(axes)):
        axes[j].axis('off')

    plt.suptitle(title, fontsize=16) # Główny tytuł wykresu
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Dostosuj układ, aby tytuł się mieścił
    plt.show()

def plot_assignment_matrix(labels, true_labels, n_clusters, title):
    """
    Tworzy i wyświetla macierz przydziału cyfr do klastrów.
    Wiersze reprezentują klastry, kolumny - prawdziwe etykiety cyfr (0-9).
    Wartości w komórkach to procent próbek danej cyfry znajdujących się w danym klastrze.
    """
    assignment_matrix = np.zeros((n_clusters, 10)) # Macierz K klastrów na 10 cyfr (0-9)

    for cluster_id in range(n_clusters):
        # Wybieramy indeksy próbek, które zostały przypisane do bieżącego klastra
        cluster_indices = np.where(labels == cluster_id)[0]
        if len(cluster_indices) > 0:
            # Pobieramy prawdziwe etykiety (cyfry) dla tych próbek
            cluster_true_labels = true_labels[cluster_indices]
            # Zliczamy wystąpienia każdej cyfry w tym klastrze
            for digit in range(10):
                count = np.sum(cluster_true_labels == digit)
                # Obliczamy procent i zapisujemy w macierzy
                assignment_matrix[cluster_id, digit] = (count / len(cluster_indices)) * 100

    plt.figure(figsize=(10, min(n_clusters, 12) * 0.8)) # Dynamiczna wysokość wykresu

    if sns is not None:
        # Użyj seaborn jeśli dostępny, dla lepszego wyglądu heatmapy
        sns.heatmap(assignment_matrix, annot=True, fmt=".1f", cmap="YlGnBu",
                    cbar_kws={'label': 'Procent próbek'}, # Etykieta paska kolorów
                    xticklabels=[str(i) for i in range(10)], # Etykiety kolumn (cyfry)
                    yticklabels=[f'Klaster {i}' for i in range(n_clusters)], # Etykiety wierszy (klastry)
                    linewidths=.5, linecolor='lightgray') # Delikatne linie siatki
    else:
        # Alternatywna wizualizacja bez seaborn
        sns_heatmap = plt.imshow(assignment_matrix, cmap='YlGnBu', aspect='auto')
        plt.colorbar(sns_heatmap, label='Procent próbek')
        plt.xticks(np.arange(10), [str(i) for i in range(10)])
        plt.yticks(np.arange(n_clusters), [f'Klaster {i}' for i in range(n_clusters)])
        # Ręczne dodawanie wartości liczbowych do heatmapy
        for i in range(n_clusters):
            for j in range(10):
                text_color = "black" if assignment_matrix[i, j] < assignment_matrix.max() / 2 else "white"
                plt.text(j, i, f'{assignment_matrix[i, j]:.1f}%',
                         ha="center", va="center", color=text_color, fontsize=8)

    plt.xlabel("Prawdziwa cyfra")
    plt.ylabel("Klaster")
    plt.title(title, fontsize=16)
    plt.tight_layout()
    plt.show()

# --- Główna logika wykonania Zadania 1 ---
if __name__ == "__main__":
    # Wczytaj dane EMNIST (cyfry)
    X_emnist, y_emnist = load_emnist_data()

    if X_emnist is None or y_emnist is None:
        print("\nProgram zakończony z powodu problemów z wczytaniem danych.")
    else:
        # Liczby klastrów do przetestowania zgodnie z zadaniem
        n_clusters_values = [10, 15, 20, 30]

        for n_clusters in n_clusters_values:
            print(f"\n--- Rozpoczynam pełną klasteryzację K-średnich dla {n_clusters} klastrów ---")
            # Inicjalizuj i dopasuj model K-średnich
            # max_iter=300 to rozsądna liczba iteracji, n_init=10 oznacza 10 prób inicjalizacji
            kmeans_model = KMeansCustom(n_clusters=n_clusters, max_iter=300, n_init=10)
            kmeans_model.fit(X_emnist)

            print(f"\nNajniższa inercja dla {n_clusters} klastrów: {kmeans_model.inertia_:.2f}")

            # 2. Przedstaw graficznie macierz przydziału cyfr do klastrów
            plot_assignment_matrix(kmeans_model.labels, y_emnist, n_clusters,
                                   f"Macierz przydziału cyfr do klastrów (K={n_clusters})")

            # 3. Wyświetl graficznie obrazy centroidów
            plot_centroids(kmeans_model.centroids,
                           f"Obrazy centroidów (K={n_clusters})")

        print("\n--- Wszystkie części Zadania 1 zakończone pomyślnie ---")