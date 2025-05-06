#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Użycie: %s <liczba_elementów>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    if (n <= 0) {
        fprintf(stderr, "Podana liczba musi być większa od zera.\n");
        return 1;
    }

    srand(time(NULL));

    printf("%d ",n);
    for (int i = n; i >= 1; i--) {
        printf("%d ", i);
    }
    printf("\n");
    
    return 0;
}
