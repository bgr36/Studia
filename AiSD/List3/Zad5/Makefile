
all: dualPivotQuickSortSelect quickSort quickSortSelect dualPivotQuickSort randomGenerator sortedGenerator reverseSortedGenerator

dualPivotQuickSortSelect: dualPivotQuickSortSelect.c
	gcc -pedantic -Wall -o dualPivotQuickSortSelect dualPivotQuickSortSelect.c

quickSort: quickSort.c
	gcc -pedantic -Wall -o quickSort quickSort.c

quickSortSelect: quickSortSelect.c
	gcc -pedantic -Wall -o quickSortSelect quickSortSelect.c

dualPivotQuickSort: dualPivotQuickSort.c
	gcc -pedantic -Wall -o dualPivotQuickSort dualPivotQuickSort.c

randomGenerator: randomGenerator.c
	gcc -pedantic -Wall -I/usr/include/gsl -L/usr/lib/x86_64-linux-gnu randomGenerator.c -lgsl -lgslcblas -lm -o randomGenerator

sortedGenerator: sortedGenerator.c
	gcc -pedantic -Wall -o sortedGenerator sortedGenerator.c

reverseSortedGenerator: reverseSortedGenerator.c
	gcc -pedantic -Wall -o reverseSortedGenerator reverseSortedGenerator.c

clean:
	rm -f dualPivotQuickSortSelect quickSort quickSortSelect dualPivotQuickSort randomGenerator sortedGenerator reverseSortedGenerator *.o
