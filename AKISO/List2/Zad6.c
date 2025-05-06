#include <stdio.h>
void printStandardColors(){
	printf("Standard Colors:");
	for (int color = 30; color <= 37; color++) {
		printf("\033[%dmHello, World!\033[0m\n",color);
	}
}

void printAllColors(){
	printf("All Colors:"); 
	for (int color = 0 ; color < 256; color++) {
		printf("\033[38;5;%dmHello, World!\033[0m\n",color);
	}
}

int main(){
	printAllColors();
	return 0;
}
