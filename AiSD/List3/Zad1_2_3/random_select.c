#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int comps = 0, swaps = 0;

void swap(int* a, int* b) {
    swaps++;
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

int partition(int arr[], int left, int right, int pivotIndex) {
    int pivotValue = arr[pivotIndex];
    swap(&arr[pivotIndex], &arr[right]); 
    int storeIndex = left;

    for (int i = left; i < right; i++) {
        comps++;
        if (arr[i] < pivotValue) {
            swap(&arr[storeIndex], &arr[i]);
            storeIndex++;
        }
    }

    swap(&arr[right], &arr[storeIndex]);  
    return storeIndex;
}

int randomized_select(int arr[], int left, int right, int k) {
    if (left == right)
        return arr[left];

    int pivotIndex = left + rand() % (right - left + 1);
    pivotIndex = partition(arr, left, right, pivotIndex);
    int order = pivotIndex - left + 1;

    if (k == order)
        return arr[pivotIndex];
    else if (k < order)
        return randomized_select(arr, left, pivotIndex - 1, k);
    else
        return randomized_select(arr, pivotIndex + 1, right, k - order);
}

int cmp(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

int main(int argc, char *argv[]) {
    srand(time(NULL));
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
    int stat = randomized_select(arr, 0, n - 1, k);
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
        printf("%d %d %d %f",n, swaps, comps, time_spent);
    }



    free(arr);
    free(original);
    return 0;
}
