#include <stdio.h>
#include <stdlib.h>
#include <gsl/gsl_rng.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>

unsigned long seed_from_urandom() {
    unsigned long seed;
    int fd = open("/dev/urandom", O_RDONLY);
    if (fd < 0 || read(fd, &seed, sizeof(seed)) != sizeof(seed)) {
        perror("read /dev/urandom");
        exit(1);
    }
    close(fd);
    return seed;
}

int random_in_range(gsl_rng *r, int max) {
    return gsl_rng_get(r) % (max + 1);  
}

int main(int argc, char *argv[]) {

    gsl_rng *r = gsl_rng_alloc(gsl_rng_mt19937);
    gsl_rng_set(r, seed_from_urandom());

    if (argc != 2) {
        fprintf(stderr, "Użycie: %s <liczba_elementów>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    if (n <= 0) {
        fprintf(stderr, "Podana liczba musi być większa od zera.\n");
        return 1;
    }

    printf("%d ",n);
    // int x = gsl_rng_get(r) % (n + 1);
    // if(x == 0) {
    //     printf("1 ");
    // }else{
    //     printf("%d ",x);
    // }

    for (int i = 0; i < n; i++) {
        printf("%d ", random_in_range(r,(2*n)-1));
    }
    printf("\n");

    gsl_rng_free(r);

    return 0;
}