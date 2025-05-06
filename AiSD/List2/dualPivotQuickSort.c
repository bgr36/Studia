#include <stdio.h>
#include <stdlib.h>

int n;
int swaps = 0;
int comps = 0;
int printThreshold = 40;

int isSorted(int arr[]) {
    for (int i = 1; i < n; i++) {
        if (arr[i - 1] > arr[i]) {
            return 0;  
        }
    }
    return 1;  
}

void print_array_step(const int *arr, int n, int step, int pivot1, int pivot2) {
    if(n < printThreshold){
        printf("Krok %02d pivoty: %02d %02d  ", step, arr[pivot1], arr[pivot2]);
        for (int i = 0; i < n; i++) {
            printf("%02d ", arr[i]);
        }
        printf("\n");
    }

}

void swap(int* a, int* b) {
    if (a != b) {
        int temp = *a;
        *a = *b;
        *b = temp;
        swaps++;
    }
}

void dualPivotQuickSort(int arr[], int low, int high, int *step) {
    if (low >= high) return;

    comps++;
    if (arr[low] > arr[high]) {
        swap(&arr[low], &arr[high]);
    }

    int p = arr[low];
    int q = arr[high];

    int lt = low + 1;
    int gt = high - 1;
    int i = lt;

    int s = 0;
    int l = 0;

    while (i <= gt) {
        if (l > s) {
            comps++;
            if (arr[i] > q) {
                swap(&arr[i], &arr[gt]);
                gt--;
                l++;
            } else {
                comps++;
                if (arr[i] < p) {
                    swap(&arr[i], &arr[lt]);
                    lt++;
                    s++;
                }
                i++;
            }
        } else {
            comps++;
            if (arr[i] < p) {
                swap(&arr[i], &arr[lt]);
                lt++;
                s++;
                i++;
            } else {
                comps++;
                if (arr[i] > q) {
                    swap(&arr[i], &arr[gt]);
                    gt--;
                    l++;
                } else {
                    i++;
                }
            }
        }
    }

    lt--;
    gt++;

    swap(&arr[low], &arr[lt]);
    swap(&arr[high], &arr[gt]);

    print_array_step(arr,n,(*step)++,lt+1,gt-1);
    dualPivotQuickSort(arr, low, lt - 1, step);     // < p
    dualPivotQuickSort(arr, lt + 1, gt - 1, step);  // p <= x <= q
    dualPivotQuickSort(arr, gt + 1, high, step);    // > q
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
    
    dualPivotQuickSort(arr, 0, n-1, &step);

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
