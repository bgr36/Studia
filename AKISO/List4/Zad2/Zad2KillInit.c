#include <stdio.h>
#include <signal.h>
#include <errno.h>
#include <string.h>

int main() {
    int pid = 1; // PID procesu init
    int signals[] = {SIGTERM, SIGKILL, SIGSTOP, SIGUSR1, SIGCONT}; // Sygnały do testowania
    size_t num_signals = sizeof(signals) / sizeof(signals[0]);

    printf("Testing signals on process with PID 1 (init):\n");

    for (size_t i = 0; i < num_signals; i++) {
        int sig = signals[i];
        printf("Sending signal %d (%s) to PID 1... ", sig, strsignal(sig));
        if (kill(pid, sig) == 0) {
            printf("Success! Signal sent.\n");
        } else {
            printf("Failed! Error: %s\n", strerror(errno));
        }
    }

    return 0;
}
