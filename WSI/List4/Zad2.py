import numpy as np
import matplotlib.pyplot as plt
import time
from torchvision import datasets, transforms

print("przygotowanie danych")
emnist_train_dataset = datasets.EMNIST(
    root='./data',
    split='digits',
    train=True,
    download=True,
)

#dane i etykiety
x_train_tensor = emnist_train_dataset.data
y_train_tensor = emnist_train_dataset.targets

x_train_numpy = x_train_tensor.numpy()
y_train_numpy = y_train_tensor.numpy()

subset_size = 10000
X = x_train_numpy[:subset_size]
y_true = y_train_numpy[:subset_size]
X_flat = X.reshape((subset_size, 784))
X_flat = X_flat.astype('float32') / 255.0

print(f"Kształt podzbioru: {X_flat.shape}")

# Implementacja DBSCAN
print("Definiowanie funkcji DBSCAN...")

UNCLASSIFIED = 0
NOISE = -1

def region_query(X, point_idx, eps):
    """
    Znajduje indeksy wszystkich punktów w sąsiedztwie `eps` danego punktu.
    """
    distances = np.linalg.norm(X - X[point_idx], axis=1)
    neighbors = np.where(distances <= eps)[0]
    return neighbors.tolist()

def expand_cluster(X, labels, point_idx, neighbors, cluster_id, eps, min_samples):
    """
    Rozszerza klaster, rekursywnie dodając sąsiadów punktów rdzeniowych.
    """
    labels[point_idx] = cluster_id
    
    i = 0
    while i < len(neighbors):
        neighbor_idx = neighbors[i]
        
        if labels[neighbor_idx] == NOISE:
            labels[neighbor_idx] = cluster_id
        elif labels[neighbor_idx] == UNCLASSIFIED:
            labels[neighbor_idx] = cluster_id
            
            new_neighbors = region_query(X, neighbor_idx, eps)
            
            if len(new_neighbors) >= min_samples:
                for nn_idx in new_neighbors:
                    if nn_idx not in neighbors:
                        neighbors.append(nn_idx)
        i += 1
        
def dbscan(X, eps, min_samples):
    """
    Główna funkcja algorytmu DBSCAN
    """
    n_points = X.shape[0]
    labels = np.full(n_points, UNCLASSIFIED)
    cluster_id = 0
    
    for point_idx in range(n_points):
        if labels[point_idx] != UNCLASSIFIED:
            continue
            
        neighbors = region_query(X, point_idx, eps)
        
        if len(neighbors) < min_samples:
            labels[point_idx] = NOISE
        else:
            cluster_id += 1
            expand_cluster(X, labels, point_idx, neighbors, cluster_id, eps, min_samples)
            
    return labels



# Parametry
MIN_SAMPLES = 15
k = MIN_SAMPLES

# Służy tylko do pomocy przy wyborze eps
# from sklearn.neighbors import NearestNeighbors
# print(f"Generowanie wykresu k-distance dla k={k}...")
# neighbors_model = NearestNeighbors(n_neighbors=k).fit(X_flat)
# distances, indices = neighbors_model.kneighbors(X_flat)
# k_distances = np.sort(distances[:, k-1], axis=0)

# plt.figure(figsize=(12, 7))
# plt.plot(k_distances)
# plt.title(f'Wykres k-distance (k={k}) dla EMNIST')
# plt.xlabel('Punkty posortowane wg odległości')
# plt.ylabel(f'Odległość do {k}-tego sąsiada')
# plt.grid(True)
# plt.show()

EPS = 5.5

print(f"Wybrane parametry: eps = {EPS}, min_samples = {MIN_SAMPLES}")

# Uruchomienie naszej implementacji DBSCAN
print("Uruchamiam DBSCAN")
start_time = time.time()
labels = dbscan(X_flat, eps=EPS, min_samples=MIN_SAMPLES)
end_time = time.time()
print(f"Koniec. Czas wykonania: {end_time - start_time:.2f} sekund.")

#Liczba klastrów i procent szumu
unique_labels, counts = np.unique(labels, return_counts=True)
n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
n_noise = np.sum(labels == -1)
noise_percentage = (n_noise / subset_size) * 100

print(f"Liczba znalezionych klastrów: {n_clusters}")
print(f"Liczba punktów szumu: {n_noise} ({noise_percentage:.2f}%)")
print("\nRozkład wielkości klastrów:")
for label, count in zip(unique_labels, counts):
    if label != NOISE:
        print(f"  Klaster {label}: {count} punktów")

# Obliczenie dokładności i błędnych klasyfikacji w klastrach
n_samples_in_clusters = subset_size - n_noise
if n_samples_in_clusters > 0:
    correct_predictions = 0
    
    cluster_to_digit_map = {}
    for cluster_id in unique_labels:
        if cluster_id == NOISE:
            continue
        
        indices_in_cluster = np.where(labels == cluster_id)[0]
        true_labels_in_cluster = y_true[indices_in_cluster]
        
        # Znajdź dominantę
        values, counts = np.unique(true_labels_in_cluster, return_counts=True)
        dominant_digit = values[np.argmax(counts)]
        cluster_to_digit_map[cluster_id] = dominant_digit

    for i in range(subset_size):
        if labels[i] != NOISE:
            predicted_digit = cluster_to_digit_map[labels[i]]
            if predicted_digit == y_true[i]:
                correct_predictions += 1
                
    accuracy = (correct_predictions / n_samples_in_clusters) * 100
    misclassification_percentage = 100 - accuracy

    print(f"Dokładność wewnątrz klastrów (na podstawie dominanty): {accuracy:.2f}%")
    print(f"Procent błędnych klasyfikacji w klastrach: {misclassification_percentage:.2f}%")
else:
    print("\nBrak klastrów do analizy")

if n_clusters > 0:
    # Wybierzmy jeden z klastrów do wizualizacji
    cluster_ids_to_show = [c_id for c_id in unique_labels if c_id != NOISE]
    
    cluster_ids_to_show.sort()

    for cluster_id_to_show in cluster_ids_to_show:
        indices_to_show = np.where(labels == cluster_id_to_show)[0]
        dominant_digit = cluster_to_digit_map[cluster_id_to_show]
        
        # Wyświetl maksymalnie 15 obrazków
        num_images = min(len(indices_to_show), 15)
        
        fig, axes = plt.subplots(3, 5, figsize=(12, 8))
        fig.suptitle(f'Przykłady z klastra nr {cluster_id_to_show} (dominująca cyfra: {dominant_digit})', fontsize=16)
        
        for i, ax in enumerate(axes.flat):
            if i < num_images:
                img_idx = indices_to_show[i]
                ax.imshow(X[img_idx], cmap='gray')
                ax.set_title(f'Prawdziwa et.: {y_true[img_idx]}')
                ax.axis('off')
            else:
                ax.axis('off')
        plt.show()
    else:
        print(f"Klaster {cluster_id_to_show} jest pusty lub nie istnieje.")
else:
    print("Brak klastrów do wizualizacji.")

print("\nZakończono cały proces.")