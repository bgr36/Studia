#include <stdio.h>
#include <stdlib.h>

int comps = 0;
int swaps = 0;
int printThreshold = 40;

// Funkcja do scalania dwóch posortowanych części tablicy
void merge(int* arr, int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;

    int* L = (int*)malloc(n1 * sizeof(int));
    int* R = (int*)malloc(n2 * sizeof(int));

    for (int i = 0; i < n1; i++) L[i] = arr[l + i];
    for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];

    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        comps++;
        if (L[i] <= R[j]) {
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
            swaps++;
        }
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];

    free(L);
    free(R);
}

// Funkcja do rekurencyjnego dzielenia tablicy na mniejsze części
void merge_sort(int* arr, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;  // Środek tablicy
        merge_sort(arr, l, m);  // Sortuj lewą część
        merge_sort(arr, m + 1, r);  // Sortuj prawą część
        merge(arr, l, m, r);  // Scal obie części
    }
}

int main(int argc, char *argv[]) {
    printThreshold = atoi(argv[1]);
    int n;
    scanf("%d", &n);
    int* arr = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);

    if(n < printThreshold){
        for (int i = 0; i < n; i++) {
            printf("%02d ", arr[i]);
        }
        printf("\n");
    }

    merge_sort(arr, 0, n - 1);

    if(n < printThreshold){
        for (int i = 0; i < n; i++) {
            printf("%02d ", arr[i]);
        }
        printf("\n");
    }

    printf("%d %d %d\n", n, swaps, comps);
    free(arr);
    return 0;
}