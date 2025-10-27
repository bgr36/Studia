import os

# Tworzymy plik z kodem bota z heurystyką łatwą do modyfikacji
bot_code = """
/****************************
Maciej Gębala (CC BY-NC 4.0)
Heuristic Bot ver. 0.1
2025-05-25
****************************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <time.h>
#include <arpa/inet.h>

#include "./board.h"

// Łatwo modyfikowalne wartości heurystyki
#define WIN_SCORE 10000
#define LOSE_SCORE -10000
#define THREE_IN_ROW_PENALTY -1000
#define THREE_IN_ROW_ENEMY_BONUS 1000

int evaluateBoard(int player) {
  // Prosty przykład: jeśli znajdziemy 4 w linii to wygrywamy, jeśli 3 to przegrywamy
  int score = 0;

  for (int i = 0; i < 5; ++i) {
    for (int j = 0; j < 2; ++j) {
      // Sprawdź poziomo
      int line[4] = { board[i][j], board[i][j+1], board[i][j+2], board[i][j+3] };
      int count = 0, opp = 0;
      for (int k = 0; k < 4; ++k) {
        if (line[k] == player) count++;
        if (line[k] == 3 - player) opp++;
      }
      if (count == 4) return WIN_SCORE;
      if (opp == 4) return LOSE_SCORE;
      if (count == 3 && opp == 0) score += THREE_IN_ROW_PENALTY;
      if (opp == 3 && count == 0) score += THREE_IN_ROW_ENEMY_BONUS;

      // Sprawdź pionowo
      line[0] = board[j][i]; line[1] = board[j+1][i]; line[2] = board[j+2][i]; line[3] = board[j+3][i];
      count = 0; opp = 0;
      for (int k = 0; k < 4; ++k) {
        if (line[k] == player) count++;
        if (line[k] == 3 - player) opp++;
      }
      if (count == 4) return WIN_SCORE;
      if (opp == 4) return LOSE_SCORE;
      if (count == 3 && opp == 0) score += THREE_IN_ROW_PENALTY;
      if (opp == 3 && count == 0) score += THREE_IN_ROW_ENEMY_BONUS;
    }
  }
  // Można dodać sprawdzanie po przekątnych analogicznie
  return score;
}

int bestMove(int player) {
  int best_score = -1000000;
  int best_move = -1;

  for (int i = 0; i < 5; ++i) {
    for (int j = 0; j < 5; ++j) {
      if (board[i][j] == 0) {
        board[i][j] = player;
        int score = evaluateBoard(player);
        board[i][j] = 0;
        if (score > best_score) {
          best_score = score;
          best_move = (i+1)*10 + (j+1);
        }
      }
    }
  }
  return best_move;
}

int main(int argc, char *argv[]) {
  int server_socket;
  struct sockaddr_in server_addr;
  char server_message[16], player_message[16];

  bool end_game;
  int player, msg, move;

  if ( argc != 5 ) {
    printf("Wrong number of arguments\\n");
    return -1;
  }

  server_socket = socket(AF_INET, SOCK_STREAM, 0);
  if ( server_socket < 0 ) {
    printf("Unable to create socket\\n");
    return -1;
  }

  server_addr.sin_family = AF_INET;
  server_addr.sin_port = htons(atoi(argv[2]));
  server_addr.sin_addr.s_addr = inet_addr(argv[1]);

  if ( connect(server_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0 ) {
    printf("Unable to connect\\n");
    return -1;
  }

  memset(server_message, '\\0', sizeof(server_message));
  if ( recv(server_socket, server_message, sizeof(server_message), 0) < 0 ) {
    printf("Error while receiving server's message\\n");
    return -1;
  }

  memset(player_message, '\\0', sizeof(player_message));
  snprintf(player_message, sizeof(player_message), "%s %s", argv[3], argv[4]);
  if ( send(server_socket, player_message, strlen(player_message), 0) < 0 ) {
    printf("Unable to send message\\n");
    return -1;
  }

  setBoard();
  end_game = false;
  sscanf(argv[3], "%d", &player);

  while ( !end_game ) {
    memset(server_message, '\\0', sizeof(server_message));
    if ( recv(server_socket, server_message, sizeof(server_message), 0) < 0 ) {
      printf("Error while receiving server's message\\n");
      return -1;
    }
    sscanf(server_message, "%d", &msg);
    move = msg%100;
    msg = msg/100;
    if ( move != 0 ) {
      setMove(move, 3-player);
    }
    if ( (msg == 0) || (msg == 6) ) {
      move = bestMove(player);
      setMove(move, player);
      memset(player_message, '\\0', sizeof(player_message));
      snprintf(player_message, sizeof(player_message), "%d", move);
      if ( send(server_socket, player_message, strlen(player_message), 0) < 0 ) {
        printf("Unable to send message\\n");
        return -1;
      }
     } else {
       end_game = true;
       switch ( msg ) {
         case 1 : printf("You won.\\n"); break;
         case 2 : printf("You lost.\\n"); break;
         case 3 : printf("Draw.\\n"); break;
         case 4 : printf("You won. Opponent error.\\n"); break;
         case 5 : printf("You lost. Your error.\\n"); break;
      }
    }
  }

  close(server_socket);
  return 0;
}
"""

# Zapiszemy go jako game_heuristic_bot.c
with open("/mnt/data/game_heuristic_bot.c", "w") as f:
    f.write(bot_code)

"/mnt/data/game_heuristic_bot.c"
