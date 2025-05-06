#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <signal.h>

#define MAX_INPUT 1024
#define MAX_ARGS 100


void sigchld_handler() {
    while (waitpid(-1, NULL, WNOHANG) > 0); 
}


void sigint_handler() {
    write(STDOUT_FILENO, "\n", 1); 
}


int parse_command(char *line, char **args, int *background) {
    int i = 0;
    *background = 0;

    char *token = strtok(line, " \t\r\n");
    while (token != NULL){

        if (strcmp(token, "&") == 0) {
            *background = 1;
        } else {
            args[i++] = token;
        }

        token = strtok(NULL, " \t\r\n");
        
    }
    args[i] = NULL;
    return i;
}


void change_directory(char **args) {
    if (args[1] == NULL) {
        fprintf(stderr, "lsh: expected argument to \"cd\"\n");
    } else if(chdir(args[1]) != 0){
        perror("lsh");   
    }
}


int handle_redirection(char **args, int *in_fd, int *out_fd, int *err_fd) {
    for (int i = 0; args[i] != NULL; i++) {
        if (strcmp(args[i], "<") == 0) {

            *in_fd = open(args[i + 1], O_RDONLY);
            if (*in_fd < 0) {

                perror("lsh: input redirection");
                return -1;

            }
            args[i] = NULL;

        } else if (strcmp(args[i], ">") == 0) {

            *out_fd = open(args[i + 1], O_WRONLY | O_CREAT | O_TRUNC, 0644);
            if (*out_fd < 0) {

                perror("lsh: output redirection");
                return -1;

            }
            args[i] = NULL;

        } else if (strcmp(args[i], "2>") == 0) {

            *err_fd = open(args[i + 1], O_WRONLY | O_CREAT | O_TRUNC, 0644);
            if (*err_fd < 0) {

                perror("lsh: error redirection");
                return -1;

            }
            args[i] = NULL;

        }
    }
    return 0;
}


void execute_command(char **args, int background) {
    int in_fd = STDIN_FILENO, out_fd = STDOUT_FILENO, err_fd = STDERR_FILENO;

    if (handle_redirection(args, &in_fd, &out_fd, &err_fd) < 0) {
        return;
    }

    pid_t pid = fork();
    if (pid == 0) { 

        if (in_fd != STDIN_FILENO) {

            dup2(in_fd, STDIN_FILENO);
            close(in_fd);

        }

        if (out_fd != STDOUT_FILENO) {

            dup2(out_fd, STDOUT_FILENO);
            close(out_fd);

        }

        if (err_fd != STDERR_FILENO) {

            dup2(err_fd, STDERR_FILENO);
            close(err_fd);

        }

        execvp(args[0], args);
        perror("lsh"); 
        exit(EXIT_FAILURE);

    } else if (pid < 0) {

        perror("lsh: fork");

    } else { 

        if (!background) {
            waitpid(pid, NULL, 0);
        }
    }
}


void execute_pipeline(char *line) {

    char *command1, *command2;
    int pipefd[2];
    pid_t pid1, pid2;

    char *pipe_pos = strchr(line, '|');

    if (pipe_pos == NULL) {

        fprintf(stderr, "No pipe found in the line\n");
        return;

    }

    *pipe_pos = '\0'; 
    command1 = line;         
    command2 = pipe_pos + 1; 

    while (*command1 == ' ') command1++;
    char *end1 = command1 + strlen(command1) - 1;
    while (end1 > command1 && (*end1 == ' ' || *end1 == '\n')) end1--;
    *(end1 + 1) = '\0'; 

    while (*command2 == ' ') command2++;
    char *end2 = command2 + strlen(command2) - 1;
    while (end2 > command2 && (*end2 == ' ' || *end2 == '\n')) end2--;
    *(end2 + 1) = '\0'; 


    if (pipe(pipefd) == -1) {

        perror("pipe");
        exit(EXIT_FAILURE);

    }

    pid1 = fork();
    if (pid1 == -1) {

        perror("fork");
        exit(EXIT_FAILURE);

    }

    if (pid1 == 0) {
        
        close(pipefd[0]); 
        dup2(pipefd[1], STDOUT_FILENO); 
        close(pipefd[1]); 

        char *args1[64]; 
        int i = 0;
        char *token = strtok(command1, " ");

        while (token != NULL) {
            args1[i++] = token;
            token = strtok(NULL, " ");
        }

        args1[i] = NULL; 

        printf("Executing command1: %s\n", command1); 
        execvp(args1[0], args1); 
        perror("execvp"); 
        exit(EXIT_FAILURE);

    } else {

        pid2 = fork();
        if (pid2 == -1) {

            perror("fork");
            exit(EXIT_FAILURE);

        }

        if (pid2 == 0) {
            
            close(pipefd[1]); 
            dup2(pipefd[0], STDIN_FILENO); 
            close(pipefd[0]); 

            char *args2[64]; 
            int j = 0;
            char *token2 = strtok(command2, " ");

            while (token2 != NULL) {
                args2[j++] = token2;
                token2 = strtok(NULL, " ");
            }

            args2[j] = NULL; 

            execvp(args2[0], args2); 
            perror("execvp"); 
            exit(EXIT_FAILURE);

        } else {
            
            close(pipefd[0]);
            close(pipefd[1]);
            waitpid(pid1, NULL, 0); 
            waitpid(pid2, NULL, 0); 

        }
    }
}


void shell_loop() {
    char line[MAX_INPUT];
    char *args[MAX_ARGS];
    int background;

    signal(SIGCHLD, sigchld_handler);
    signal(SIGINT, sigint_handler);

    while (1) {
        printf("lsh> ");
        if (fgets(line, sizeof(line), stdin) == NULL) {
            break;
        }

        if (strchr(line, '|')) {
            execute_pipeline(line);
            continue;
        }

        int argc = parse_command(line, args, &background);
        if (argc == 0) {
            continue;
        }

        if (strcmp(args[0], "exit") == 0) {
            break;
        } else if (strcmp(args[0], "cd") == 0) {
            change_directory(args);
        } else {
            execute_command(args, background); 
        }
    }
}

int main() {
    shell_loop();
    return 0;
}
