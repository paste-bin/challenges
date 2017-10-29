// Basic network sockets challenge
// You have to connect to a socket on a port, do something that requires more than just netcat, then get the flag
// Andrew Bennett
// 2016-03-27
// Freelancer CTF

#include <stdio.h>

#define TRUE (1==1)
#define FALSE (1==0)

int mostBasic();
void win();
void lose();

int main (int argc, char *argv[]) {
  if (mostBasic() == TRUE) {
    win();
  } else {
    lose();
  } 

  return 0;
}

int mostBasic() {
  char input[20];

  printf("Awaiting input:\n");
  fflush(stdout);
  fgets(input, 15, stdin);

  if (strcmp(input, "FLAG?") == 0 ||
      strcmp(input, "FLAG?\n") == 0 ||
      strcmp(input, "FLAG?\r\n") == 0) {
    return TRUE;
  } else {
  }

  return FALSE;
}

void win() {
  printf("\nYou win!\nThe flag is: flag{asdf}\n");
  fflush(stdout);
}

void lose() {
  printf("Incorrect, byebye.\n");
  fflush(stdout);
}
