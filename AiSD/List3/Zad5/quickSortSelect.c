#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int n;
int swaps = 0;
int comps = 0;
int printThreshold = 40;

void swap(int *a, int *b) {
    swaps++;
    int temp = *a;
    *a = *b;
    *b = temp;
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

int partition_with_pivot(int arr[], int left, int right, int pivot) {
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
    int i, median[(n + 4) / 5];
    for (i = 0; i < n / 5; i++) {
        insertion_sort(arr, left + i * 5, left + i * 5 + 4);
        median[i] = arr[left + i * 5 + 2];
    }
    if (i * 5 < n) {
        insertion_sort(arr, left + i * 5, right);
        median[i] = arr[left + i * 5 + (right - (left + i * 5)) / 2];
        i++;
    }

    int medOfMed = (i == 1) ? median[0] : select_deterministic(median, 0, i - 1, i / 2);

    int pivotIndex = partition_with_pivot(arr, left, right, medOfMed);
    int rank = pivotIndex - left + 1;

    if (k == rank)
        return arr[pivotIndex];
    else if (k < rank)
        return select_deterministic(arr, left, pivotIndex - 1, k);
    else
        return select_deterministic(arr, pivotIndex + 1, right, k - rank);
}

void print_array_step(const int *arr, int n, int step, int pivot) {
    if(n < printThreshold){
        printf("Krok %02d : ", step);
        for (int i = 0; i < n; i++) {
            if(i == pivot){
                printf("[%02d] ", arr[i]);
            } else {
                printf("%02d ", arr[i]);
            }
        }
        printf("\n");
    }
}

void quickSort(int arr[], int low, int high, int *step) {
    if (low < high) {
        int length = high - low + 1;
        int mid = (length + 1) / 2; // szukamy mediany
        
        int pivot = select_deterministic(arr, low, high, mid);
        int pi = partition_with_pivot(arr, low, high, pivot);

        print_array_step(arr, n, (*step)++, pi);

        quickSort(arr, low, pi - 1, step);
        quickSort(arr, pi + 1, high, step);
    }
}

int isSorted(int arr[]) {
    for (int i = 1; i < n; i++) {
        if (arr[i - 1] > arr[i]) {
            return 0;  
        }
    }
    return 1;  
}

int main(int argc, char *argv[]) {
    if (argc > 1)
        printThreshold = atoi(argv[1]);
    
    int step = 1;
    scanf("%d", &n);
    int *arr = malloc(n * sizeof(int));
    int *orgArr = malloc(n * sizeof(int));

    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        arr[i] = x;
        orgArr[i] = x;
    }

    if (n < printThreshold) {
        for (int i = 0; i < n; i++) {
            printf("%02d ", orgArr[i]);
        }
        printf("\n");
    }

    quickSort(arr, 0, n - 1, &step);

    if (n < printThreshold) {
        for (int i = 0; i < n; i++) {
            printf("%02d ", arr[i]);
        }
        printf("\n");
        printf("Tablica posortowana: %d \n", isSorted(arr));
    }
    
    printf("%d %d %d \n", n, swaps, comps);

    free(arr);
    free(orgArr);

    return 0;
}
