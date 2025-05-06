#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <PID>\n", argv[0]);
        return 1;
    }

    int pid = atoi(argv[1]);
    int num_signals = 100;

    printf("Sending %d SIGUSR1 signals to process %d...\n", num_signals, pid);
    for (int i = 0; i < num_signals; i++) {
        kill(pid, SIGUSR1);
    }

    printf("Signals sent. Check the receiver output.\n");
    return 0;
}
