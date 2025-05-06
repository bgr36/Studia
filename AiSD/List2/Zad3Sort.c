#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int comps = 0;
int swaps = 0;
int printThreshold = 40;

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

// Znajdź rosnące "runy" i zapisz ich zakresy w tablicy
int find_runs(int* arr, int n, int (*runs)[2]) {
    int count = 0;
    int start = 0;
    for (int i = 1; i <= n; i++) {
        if (i == n || arr[i] < arr[i - 1]) {
            runs[count][0] = start;
            runs[count][1] = i - 1;
            count++;
            start = i;
        }
    }
    return count;
}

void merge_runs(int* arr, int (*runs)[2], int count) {
    while (count > 1) {
        int new_count = 0;
        for (int i = 0; i + 1 < count; i += 2) {
            merge(arr, runs[i][0], runs[i][1], runs[i + 1][1]);
            runs[new_count][0] = runs[i][0];
            runs[new_count][1] = runs[i + 1][1];
            new_count++;
        }
        if (count % 2 == 1) {
            runs[new_count][0] = runs[count - 1][0];
            runs[new_count][1] = runs[count - 1][1];
            new_count++;
        }
        count = new_count;
    }
}

void my_merge_sort(int* arr, int n) {
    int (*runs)[2] = malloc(sizeof(int[2]) * n);
    int count = find_runs(arr, n, runs);
    merge_runs(arr, runs, count);
    free(runs);
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

    my_merge_sort(arr, n);

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
