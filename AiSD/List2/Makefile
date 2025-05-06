
all: mergeSort Zad3Sort insertionSort quickSort hybridSort dualPivotQuickSort randomGenerator sortedGenerator reverseSortedGenerator

insertionSort: insertionSort.c
	gcc -pedantic -Wall -o insertionSort insertionSort.c

quickSort: quickSort.c
	gcc -pedantic -Wall -o quickSort quickSort.c

hybridSort: hybridSort.c
	gcc -pedantic -Wall -o hybridSort hybridSort.c

dualPivotQuickSort: dualPivotQuickSort.c
	gcc -pedantic -Wall -o dualPivotQuickSort dualPivotQuickSort.c

randomGenerator: randomGenerator.c
	gcc -pedantic -Wall -I/usr/include/gsl -L/usr/lib/x86_64-linux-gnu randomGenerator.c -lgsl -lgslcblas -lm -o randomGenerator

sortedGenerator: sortedGenerator.c
	gcc -pedantic -Wall -o sortedGenerator sortedGenerator.c

reverseSortedGenerator: reverseSortedGenerator.c
	gcc -pedantic -Wall -o reverseSortedGenerator reverseSortedGenerator.c

mergeSort: mergeSort.c
	gcc -pedantic -Wall -o mergeSort mergeSort.c

Zad3Sort: Zad3Sort.c
	gcc -pedantic -Wall -o Zad3Sort Zad3Sort.c

clean:
	rm -f insertionSort quickSort hybridSort dualPivotQuickSort randomGenerator sortedGenerator reverseSortedGenerator Zad3Sort mergeSort *.o
