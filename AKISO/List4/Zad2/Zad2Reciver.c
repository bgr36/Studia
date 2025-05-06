#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>

// Liczniki sygnałów
volatile sig_atomic_t sigusr1_count = 0;
volatile sig_atomic_t sigrt_count = 0;

// Funkcja obsługi SIGUSR1
void handle_sigusr1(int signum) {
    sigusr1_count++;
    printf("Received SIGUSR1. Total count: %d\n", sigusr1_count);
}

// Funkcja obsługi SIGRTMIN
void handle_sigrt(int signum) {
    sigrt_count++;
    printf("Received SIGRTMIN. Total count: %d\n", sigrt_count);
}

int main() {
    // Rejestracja handlerów dla sygnałów
    struct sigaction sa_usr1, sa_rt;

    // Handler dla SIGUSR1
    sa_usr1.sa_handler = handle_sigusr1;
    sa_usr1.sa_flags = 0;
    sigemptyset(&sa_usr1.sa_mask);
    sigaction(SIGUSR1, &sa_usr1, NULL);

    // Handler dla SIGRTMIN
    // sa_rt.sa_handler = handle_sigrt;
    // sa_rt.sa_flags = 0;
    // sigemptyset(&sa_rt.sa_mask);
    // sigaction(SIGRTMIN, &sa_rt, NULL);

    printf("Process PID: %d\n", getpid());
    printf("Waiting for signals...\n");

    // Czekanie na sygnały
    while (1) {
        pause(); // Zawieszenie procesu do momentu odebrania sygnału
    }

    return 0;
}
