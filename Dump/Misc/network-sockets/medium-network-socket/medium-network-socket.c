// Basic network sockets challenge
// You have to connect to a socket on a port, do something that requires more than just netcat, then get the flag
// Andrew Bennett
// 2016-03-27
// Freelancer CTF

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <unistd.h>
#include <signal.h>
#include <sys/signal.h>

#define TRUE (1==1)
#define FALSE (1==0)

#define NUM_ANSWERS 3

int medium();

int chain();
void setupChallenges();

void win();
void lose();
void alarm_handler(int signum);

//char *challenges[20];
//char *answers[20];

char *challenges[NUM_ANSWERS] = {
    "What is 1 + 2 ?",
    "What is 4 * 1 ?",
    "What is 8 * 2 ?"
};
char *answers[NUM_ANSWERS] = {
    "3",
    "4",
    "16"
};


int main (int argc, char *argv[]) {

  signal(SIGALRM, alarm_handler);

  setupChallenges();

  if (chain() == TRUE) {
    win();
  } else {
    lose();
  } 

  return 0;
}

void setupChallenges() {
  srand(time(NULL));
  
}

void alarm_handler(int signum) {
  printf("Too slow!\nByebye.\n");
  fflush(stdout);
  exit(0);
}

int doChallenge(int currTimeout, int u) {

  char input[20];
  int randNum = 0;
  randNum = rand()%NUM_ANSWERS;

  printf("%s\n", challenges[randNum]);
  fflush(stdout);


  if (u == 1) {
    ualarm(currTimeout, 0);
    printf("Current timeout in seconds: %lf\n", (float)currTimeout/1000000);
  } else {
    alarm(currTimeout);
    printf("Current timeout: %d\n", currTimeout);
  }

  fgets(input, 15, stdin);

  if (strcmp(input, answers[randNum]) == 0 ||
      strcmp(input, strcat(strdup(answers[randNum]), "\n")) == 0 || 
      strcmp(input, strcat(strdup(answers[randNum]), "\r\n")) == 0) {
    return TRUE;
  } else {
    lose();
  }

  return FALSE;
}

int chain() {
  // grab a challenge, make them solve it, getting faster and faster
  int currTimeout = 10; 
  
  while (currTimeout > 0) {
    doChallenge(currTimeout, 0);

    currTimeout -= 2;
  }

  // now let's do 5 challenges with 1 second each
  for (int i=0; i<5; i++) {
    doChallenge(1, 0);
  }

  /* too hard?
  // made it through the easy part, time to step it up
  currTimeout = 999999;

  for (int i=0; i<20; i++) {
    doChallenge(currTimeout, 1);
    if (i % 5 == 0) {
      currTimeout -= 100000;
    }
  }
  */

  return TRUE;
}

void win() {
  printf("\nYou win!\nThe flag is: flag{asdf}\n");
  fflush(stdout);
}

void lose() {
  printf("Incorrect, byebye.\n");
  fflush(stdout);
  exit(0);
}
