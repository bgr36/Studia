# Reguła domyślna (kompilacja wszystkich plików)
all: randomGenerator random_select select3 select7 select9 select

# Kompilacja randomGenerator.c
randomGenerator: randomGenerator.c
	gcc -pedantic -Wall -I/usr/include/gsl -L/usr/lib/x86_64-linux-gnu randomGenerator.c -lgsl -lgslcblas -lm -o randomGenerator

# Kompilacja random_select.c
random_select: random_select.c
	gcc -Wall -pedantic random_select.c -o random_select

# Kompilacja select3.c
select3: select3.c
	gcc -Wall -pedantic select3.c -o select3

# Kompilacja select7.c
select7: select7.c
	gcc -Wall -pedantic select7.c -o select7

# Kompilacja select9.c
select9: select9.c
	gcc -Wall -pedantic select9.c -o select9

# Kompilacja select.c
select: select.c
	gcc -Wall -pedantic select.c -o select

# Reguła czyszcząca pliki wynikowe
clean:
	rm -f randomGenerator random_select select3 select7 select9 select

.PHONY: all clean
