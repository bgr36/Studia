#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>

void signal_handler(int signum) {
    printf("Received signal: %d\n", signum);
    if (signum == SIGINT) {
        exit(0); // Wyjście z programu przy SIGINT (Ctrl+C)
    }
}

int main() {
    // Obsługa wszystkich sygnałów
    for (int i = 1; i < NSIG; i++) {
        if (signal(i, signal_handler) == SIG_ERR) {
            printf("Cannot handle signal: %d\n", i);
        }
    }

    printf("Process PID: %d\n", getpid());
    while (1) {
        pause(); // Oczekiwanie na sygnały
    }

    return 0;
}
