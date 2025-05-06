#include <stdio.h>
#include <stdlib.h>

int comps = 0;  // Zmienna do zliczania liczby porównań


int binarySearch(int arr[], int v, int low, int high) {
    if (low > high) {
        return 0;  
    }

    int mid = low + (high - low) / 2;
    comps++;  

    if (arr[mid] == v) {
        return 1;  
    }

    if (arr[mid] > v) {
        return binarySearch(arr, v, low, mid - 1);  
    } else {
        return binarySearch(arr, v, mid + 1, high);  
    }
}

int main(int argc, char *argv[]) {
    int n, v;
    v = atoi(argv[1]);
    scanf("%d ", &n);

    int* arr = malloc(n * sizeof(int));
    int* original = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
        original[i] = arr[i];
    }

    int result = binarySearch(arr,v,-0,n-1);

    if (n <= 30) {
        printf("Końcowy stan tablicy:\n");
        for (int i = 0; i < n; i++) printf("%d ", arr[i]);
        printf("\n");
    }

    

    if (n <= 30) {
        printf("Znaleziono element %d : %d \n",v,result);
        printf("\n");
        printf("Porównań: %d\n", comps);
    }else{
        printf("%d %d \n", n, comps);
    }


    free(arr);
    free(original);
    return 0;
}