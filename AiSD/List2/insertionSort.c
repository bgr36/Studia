#include <stdio.h>
#include <stdlib.h>

int swaps = 0;
int comps = 0;
int printThreshold = 40;

int isSorted(int arr[], int n) {
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

void insertionSort(int arr[], int n) {
    int step = 0;
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        comps++;
        while (j >= 0 && arr[j] > key) {
            comps++;
            arr[j + 1] = arr[j];
            swaps++;
            j--;
        }
        swaps++;
        arr[j + 1] = key;
        print_array_step(arr,n,step++);
    }
}

int main(int argc, char *argv[]) {
    printThreshold = atoi(argv[1]);
    int n;
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
    
    insertionSort(arr, n);

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
        printf("Tablica posortowana: %d\n",isSorted(arr,n));
    }
    

    // FILE *file = fopen("insertion_sort_results","a");
    // if(file == NULL){
    //     perror("File error");
    //     return 1;
    // }
    // fprintf(file,"%d, %d, %d \n",n,comps,swaps);
    // fclose(file);

 
    printf("%d %d %d\n",n,swaps,comps);
    
    return 0;
}
