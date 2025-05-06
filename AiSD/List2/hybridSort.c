#include <stdio.h>
#include <stdlib.h>

int n;
int swaps = 0;
int comps = 0;
int threshold = 5;
int printThreshold = 40;

int isSorted(int arr[]) {
    for (int i = 1; i < n; i++) {
        if (arr[i - 1] > arr[i]) {
            return 0;  
        }
    }
    return 1;  
}

void print_array_step(const int *arr, int n, int step) {
    if(n < printThreshold){
        printf("Krok %02d: ", step);
        for (int i = 0; i < n; i++) {
            printf("%02d ", arr[i]);
        }
        printf("\n"); 
    }
}

void print_array_step_q(const int *arr, int n, int step, int pivot) {
    if(n < printThreshold){
        printf("Krok %02d: ", step);
        for (int i = 0; i < n; i++) {
            if(i == pivot){
                printf("[%02d] ", arr[i]);
            }else{
                printf("%02d ", arr[i]);
            }
        }
        printf("\n");
    }
}

void insertionSort(int arr[], int low, int high,int *step) {
    for (int i = low + 1; i <= high; i++) {
        int key = arr[i];
        int j = i - 1;
        comps++;
        while (j >= low && arr[j] > key) {
            comps++;
            arr[j + 1] = arr[j];
            swaps++;
            j--;
        }
        swaps++;
        arr[j + 1] = key;
        print_array_step(arr,n,(*step)++);
    }
}

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
    swaps++;
}

int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        comps++;
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}

void hybridQuickSort(int arr[], int low, int high,int *step) {
    while (low < high) {
        if (high - low < threshold) {
            insertionSort(arr, low, high, step);
            break;
        } else {
            int pi = partition(arr, low, high);
            print_array_step_q(arr,n,(*step)++,pi);
            if (pi - low < high - pi) {
                hybridQuickSort(arr, low, pi - 1, step);
                low = pi + 1;
            } else {
                hybridQuickSort(arr, pi + 1, high, step);
                high = pi - 1;
            }
        }
    }
}

int main(int argc, char *argv[]) {
    printThreshold = atoi(argv[1]);
    int step = 1;
    scanf("%d", &n);
    int arr[n];
    int orgArr[n];
    for (int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        arr[i] = x;
        orgArr[i] = x;
    }

    if(n < printThreshold){
        for (int i = 0; i < n; i++) {
            printf("%02d ", orgArr[i]);
        }
        printf("\n");
    }
    
    hybridQuickSort(arr, 0, n-1, &step);

    if(n < printThreshold){
        for (int i = 0; i < n; i++) {
            printf("%02d ", orgArr[i]);
        }
        printf("\n");
    }

    if(n < printThreshold){
        for (int i = 0; i < n; i++) {
            printf("%02d ", arr[i]);
        }
        printf("\n");
        printf("Tablica posortowana: %d\n",isSorted(arr));
    }

    printf("%d %d %d\n",n,swaps,comps);

    return 0;
}
