#include <stdio.h>
#include <stdlib.h>

int n;
int swaps = 0;
int comps = 0;
int printThreshold = 40;

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
    swaps++;
}

void print_array_step(const int *arr, int n, int step, int pivot1, int pivot2) {
    if (n < printThreshold) {
        printf("Krok %02d : ", step);
        for (int i = 0; i < n; i++) {
            if (i == pivot1 || i == pivot2) {
                printf("[%02d] ", arr[i]);
            } else {
                printf("%02d ", arr[i]);
            }
        }
        printf("\n");
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

int findMedian(int arr[], int l, int n) {
    for (int i = l; i < l + n; i++) {
        for (int j = i + 1; j < l + n; j++) {
            comps++;
            if (arr[i] > arr[j]) {
                swap(&arr[i], &arr[j]);
            }
        }
    }
    return arr[l + n/2];
}

int selectPivot(int arr[], int l, int r) {
    int n = r - l + 1;
    int median[(n+4)/5];
    int i;
    for (i = 0; i < n/5; i++) {
        median[i] = findMedian(arr, l + i*5, 5);
    }
    if (i*5 < n) {
        median[i] = findMedian(arr, l + i*5, n%5);
        i++;
    }

    int medOfMed;
    if (i == 1)
        medOfMed = median[i-1];
    else
        medOfMed = selectPivot(median, 0, i-1);

    for (int j = l; j <= r; j++) {
        if (arr[j] == medOfMed)
            return j;
    }
    return -1;
}

void dualPivotQuickSort(int arr[], int low, int high, int *step) {
    if (low < high) {
        int pivot1Index = selectPivot(arr, low, high);
        int pivot2Index = selectPivot(arr, low, high);

        if (pivot1Index == pivot2Index)
            pivot2Index = high;

        swap(&arr[low], &arr[pivot1Index]);
        swap(&arr[high], &arr[pivot2Index]);

        comps++;
        if (arr[low] > arr[high])
            swap(&arr[low], &arr[high]);

        int pivot1 = arr[low];
        int pivot2 = arr[high];

        int i = low + 1;
        int lt = low + 1;
        int gt = high - 1;

        while (i <= gt) {
            comps++;
            if (arr[i] < pivot1) {
                swap(&arr[i], &arr[lt]);
                lt++;
            } else if (arr[i] > pivot2) {
                swap(&arr[i], &arr[gt]);
                gt--;
                i--;
            }
            i++;
        }

        lt--;
        gt++;

        swap(&arr[low], &arr[lt]);
        swap(&arr[high], &arr[gt]);

        print_array_step(arr, n, (*step)++, lt, gt);

        dualPivotQuickSort(arr, low, lt - 1, step);
        dualPivotQuickSort(arr, lt + 1, gt - 1, step);
        dualPivotQuickSort(arr, gt + 1, high, step);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <printThreshold>\n", argv[0]);
        return 1;
    }

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

    if (n < printThreshold) {
        for (int i = 0; i < n; i++) {
            printf("%02d ", orgArr[i]);
        }
        printf("\n");
    }

    dualPivotQuickSort(arr, 0, n - 1, &step);

    if (n < printThreshold) {
        for (int i = 0; i < n; i++) {
            printf("%02d ", orgArr[i]);
        }
        printf("\n");
        for (int i = 0; i < n; i++) {
            printf("%02d ", arr[i]);
        }
        printf("\n");
        printf("Tablica posortowana: %d\n", isSorted(arr));
    }

    printf("%d %d %d\n", n, swaps, comps);

    return 0;
}
