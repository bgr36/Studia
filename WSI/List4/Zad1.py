import numpy as np
import matplotlib.pyplot as plt
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import seaborn as sns

def load_emnist_data():
    X = None
    y = None

    print("przygotowywanie danych")
    emnist_train = datasets.EMNIST(root='./data', split='digits', train=True, download=True,
                                    transform=transforms.ToTensor())

    X_list = []
    y_list = []
    for i, (img, label) in enumerate(emnist_train):
        X_list.append(img.numpy().flatten())
        y_list.append(label)

    X = np.array(X_list).astype(float)
    y = np.array(y_list)

    print(f"Zakończono wczytywanie.")

    return X, y

#Klasa KMeansCustom: Samodzielna implementacja K-średnich
class KMeansCustom:
    def __init__(self, n_clusters, max_iter=300, n_init=10):

        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.n_init = n_init
        self.centroids = None
        self.labels = None
        self.inertia_ = float('inf')

    def _euclidean_distance(self, point1, point2):
        return np.sqrt(np.sum((point1 - point2)**2))

    def _calculate_inertia(self, X, labels, centroids):
        inertia = 0
        for i in range(self.n_clusters):
            cluster_points = X[labels == i]
            if len(cluster_points) > 0:
                inertia += np.sum(np.sum((cluster_points - centroids[i])**2, axis=1))
        return inertia

    def _initialize_centroids_kmeans_plusplus(self, X):
        n_samples, n_features = X.shape
        centroids = np.zeros((self.n_clusters, n_features))

        #Wybierz pierwszy centroid losowo
        first_centroid_idx = np.random.randint(0, n_samples)
        centroids[0] = X[first_centroid_idx]

        for i in range(1, self.n_clusters):
            distances_sq = np.zeros(n_samples)
            for j in range(n_samples):
                min_dist_sq = float('inf')
                for c_idx in range(i):
                    dist_sq = np.sum((X[j] - centroids[c_idx])**2)
                    if dist_sq < min_dist_sq:
                        min_dist_sq = dist_sq
                distances_sq[j] = min_dist_sq


            sum_distances_sq = np.sum(distances_sq)
            if sum_distances_sq == 0:
                probabilities = np.ones(n_samples) / n_samples 
            else:
                probabilities = distances_sq / sum_distances_sq

            new_centroid_idx = np.random.choice(n_samples, p=probabilities)
            centroids[i] = X[new_centroid_idx]
        return centroids
    
    #Dopasowuje algorytm K-średnich
    def fit(self, X):
        best_centroids = None
        best_labels = None
        best_inertia = float('inf')

        # Wykonaj wiele prób inicjalizacji, aby znaleźć klasteryzację o najmniejszej inercji
        for init_attempt in range(self.n_init):
            print(f"\n  Rozpoczynam próbę inicjalizacji {init_attempt + 1}/{self.n_init}...")
            print(f"  Inicjalizowanie centroidów metodą k-means++")
            current_centroids = self._initialize_centroids_kmeans_plusplus(X)
            print(f"  Centroidy zainicjalizowane. Rozpoczynam iteracje")

            current_labels = np.zeros(X.shape[0], dtype=int)

            for iteration in range(self.max_iter):
                # Przypisanie każdego punktu do najbliższego centroidu
                new_labels = np.zeros(X.shape[0], dtype=int)
                for i, point in enumerate(X):
                    distances = [self._euclidean_distance(point, c) for c in current_centroids]
                    new_labels[i] = np.argmin(distances)

                # Obliczanie nowych centroidów
                new_centroids = np.zeros_like(current_centroids)
                for i in range(self.n_clusters):
                    cluster_points = X[new_labels == i]
                    if len(cluster_points) > 0:
                        new_centroids[i] = np.mean(cluster_points, axis=0) # Oblicz średnią punktów w klastrze
                    else:
                        # Zainicjuj centroid losowym punktem z danych, aby uniknąć błędów i spróbować "ożywić" klaster.
                        new_centroids[i] = X[np.random.randint(0, X.shape[0])]

                # Sprawdzenie zbieżności
                if np.allclose(new_centroids, current_centroids, atol=1e-6):
                    print(f"    Zbieżność osiągnięta w iteracji {iteration + 1}.")
                    break 
                current_centroids = new_centroids
                current_labels = new_labels

                
                print(f"    Iteracja {iteration + 1}/{self.max_iter} zakończona...")

            # Oblicz inercję dla bieżącej próby inicjalizacji
            current_inertia = self._calculate_inertia(X, current_labels, current_centroids)
            print(f"  Zakończono próbę {init_attempt + 1}. Inercja: {current_inertia:.2f}")

            # Zaktualizuj najlepsze wyniki, jeśli bieżąca inercja jest niższa
            if current_inertia < best_inertia:
                best_inertia = current_inertia
                best_centroids = current_centroids
                best_labels = current_labels
                print(f"Nowa najlepsza inercja: {best_inertia:.2f}")

        self.centroids = best_centroids
        self.labels = best_labels
        self.inertia_ = best_inertia
        print("\nKlasteryzacja K-średnich zakończona.")

def plot_centroids(centroids, title):

    num_centroids = len(centroids)
    # Oblicz optymalną siatkę wyświetlania dla lepszej czytelności
    n_cols = min(num_centroids, 10)
    n_rows = (num_centroids + n_cols - 1) // n_cols 

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(2 * n_cols, 2 * n_rows))
    axes = axes.flatten() if n_rows > 1 or n_cols > 1 else [axes]

    for i, centroid in enumerate(centroids):
        # Spłaszczony wektor 784 elementów jest przekształcany na obraz 28x28
        axes[i].imshow(centroid.reshape(28, 28), cmap='gray_r')
        axes[i].axis('off') 
        axes[i].set_title(f'C {i}') 

    # Wyłącz pozostałe puste sub-wykresy, jeśli jest ich mniej niż siatka
    for j in range(num_centroids, len(axes)):
        axes[j].axis('off')

    plt.suptitle(title, fontsize=16) 
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 
    plt.show()

def plot_assignment_matrix(labels, true_labels, n_clusters, title):

    assignment_matrix = np.zeros((n_clusters, 10))

    for cluster_id in range(n_clusters):
        cluster_indices = np.where(labels == cluster_id)[0]
        if len(cluster_indices) > 0:
            cluster_true_labels = true_labels[cluster_indices]
            for digit in range(10):
                count = np.sum(cluster_true_labels == digit)
                assignment_matrix[cluster_id, digit] = (count / len(cluster_indices)) * 100

    plt.figure(figsize=(10, min(n_clusters, 12) * 0.8))

    sns.heatmap(assignment_matrix, annot=True, fmt=".1f", cmap="YlGnBu",
                cbar_kws={'label': 'Procent próbek'},
                xticklabels=[str(i) for i in range(10)],
                yticklabels=[f'Klaster {i}' for i in range(n_clusters)],
                linewidths=.5, linecolor='lightgray')

    plt.xlabel("Prawdziwa cyfra")
    plt.ylabel("Klaster")
    plt.title(title, fontsize=16)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    X_emnist, y_emnist = load_emnist_data()

    n_clusters_values = [10, 15, 20, 30]

    for n_clusters in n_clusters_values:
        print(f"\n--- Rozpoczynam pełną klasteryzację K-średnich dla {n_clusters} klastrów ---")

        kmeans_model = KMeansCustom(n_clusters=n_clusters, max_iter=50, n_init=10)
        kmeans_model.fit(X_emnist)

        print(f"\nNajniższa inercja dla {n_clusters} klastrów: {kmeans_model.inertia_:.2f}")

        plot_assignment_matrix(kmeans_model.labels, y_emnist, n_clusters,
                                f"Macierz przydziału cyfr do klastrów (K={n_clusters})")

        plot_centroids(kmeans_model.centroids,
                        f"Obrazy centroidów (K={n_clusters})")

    print("\n--- Wszystkie części Zadania 1 zakończone pomyślnie ---")