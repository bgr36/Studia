#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int comps = 0, swaps = 0;

void swap(int* a, int* b) {
    swaps++;
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

void insertion_sort(int arr[], int left, int right) {
    for (int i = left + 1; i <= right; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= left && arr[j] > key) {
            comps++;
            arr[j + 1] = arr[j];
            swaps++;
            j--;
        }
        arr[j + 1] = key;
    }
}

int partition(int arr[], int left, int right, int pivot) {
    int pivotIndex;
    for (pivotIndex = left; pivotIndex <= right; pivotIndex++) {
        comps++;
        if (arr[pivotIndex] == pivot)
            break;
    }
    swap(&arr[pivotIndex], &arr[right]);

    int store = left;
    for (int i = left; i < right; i++) {
        comps++;
        if (arr[i] < pivot) {
            swap(&arr[i], &arr[store]);
            store++;
        }
    }
    swap(&arr[store], &arr[right]);
    return store;
}

int select_deterministic(int arr[], int left, int right, int k) {
    if (left == right)
        return arr[left];

    int n = right - left + 1;

    int i, median[(n + 8) / 9];

    for (i = 0; i < n / 9; i++) {
        insertion_sort(arr, left + i * 9, left + i * 9 + 8);
        median[i] = arr[left + i * 9 + 4];
    }

    if (i * 9 < n) {
        insertion_sort(arr, left + i * 9, right);
        median[i] = arr[left + i * 9 + (right - (left + i * 9)) / 2];
        i++;
    }
    

    int medOfMed = (i == 1) ? median[0] : select_deterministic(median, 0, i - 1, i / 2);

    int pivotIndex = partition(arr, left, right, medOfMed);
    int rank = pivotIndex - left + 1;

    if (k == rank)
        return arr[pivotIndex];
    else if (k < rank)
        return select_deterministic(arr, left, pivotIndex - 1, k);
    else
        return select_deterministic(arr, pivotIndex + 1, right, k - rank);
}

int cmp(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

int main(int argc, char *argv[]) {
    int n, k;
    k = atoi(argv[1]);
    scanf("%d ", &n);

    int* arr = malloc(n * sizeof(int));
    int* original = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
        original[i] = arr[i];
    }

    if (n <= 30) {
        printf("Początkowy stan tablicy:\n");
        for (int i = 0; i < n; i++) printf("%d ", arr[i]);
        printf("\n");
    }

    clock_t start_time = clock();
    int stat = select_deterministic(arr, 0, n - 1, k);
    clock_t end_time = clock();
    double time_spent = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    if (n <= 30) {
        printf("Końcowy stan tablicy:\n");
        for (int i = 0; i < n; i++) printf("%d ", arr[i]);
        printf("\n");
    }

    

    qsort(original, n, sizeof(int), cmp);

    if (n <= 30) {
        printf("Posortowany ciąg:\n");
        for (int i = 0; i < n; i++) printf("%d ", original[i]);
        printf("\n");
        printf("Porównań: %d\nPrzestawień: %d\n", comps, swaps);
        printf("Znaleziony element jako %d-ta statystyka pozycyjna: %d\n", k, stat);
    }else{
        printf("%d %d %d %f \n",n, swaps, comps, time_spent);
    }


    free(arr);
    free(original);
    return 0;
}
