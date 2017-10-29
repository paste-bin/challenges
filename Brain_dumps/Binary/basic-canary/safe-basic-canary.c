// Basic Canary
// Andrew Bennett
// 2016-03-26
// Written for the Freelancer CTF
// 
// this is a "safe" way of running it to emulate the expected behavior
// might make smash stacking safer :)
// compile WITHOUT turning off the stack protector (leave it on!)

#include <stdio.h>
#include <stdlib.h>

void setup();
void printArray(int array[]);
void thank();
void win();

char *flags[5];

int main(int argc, char *argv[]) {

  printf("Welcome to <challenge name>!\n\n");
  fflush(stdout);
  setup();

  // unused int secret = 5;
  int array[12] = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 1, 1};
  // array[11] is num / if you overflow that you'll mess with num
  // array[10] is secret / the flag one
  int num;
  
  printf("How many numbers would you like to scan in? ");
  fflush(stdout);
  scanf("%d", &num); 

  for (int i=0; i<num; i++) {
    printf("\nEnter a number: ");
    fflush(stdout);
    int in;
    scanf("%d", &in);
    if (i < 12) {
      array[i] = in;
    }
    thank();
  }

  if (num >= 12) {
    printf("\nSegmentation fault\n");
    fflush(stdout);
    exit(0);
  }
  printArray(array);

  if (array[10] == 0x41414141) {
    win();
  }

  return 0;
}

void printArray(int array[]) {
  printf("\nThe array contains:\n");
  for (int i=0; i<10; i++) {
    printf("%d ", array[i]);
  }
  printf("\n");
}

void setup() {
  srand(91066);
  flags[0] = "you-tried";
  flags[1] = "y0l0";
  flags[2] = "h4ck the plan3t!";
  flags[3] = "0x41414141";
  flags[4] = "w1nn3r";
}

char *whichFlag() {
  return flags[rand()%5];
}

void thank() {
  int random = rand()%13;
  switch (random) {
    case 0:
      printf("The flag is flag{%s}.... or is it?\n", whichFlag());
      break;
    case 1:
    case 2:
    case 3:
    case 4:
      printf("Awesome!\n");
      break;
    case 5:
    case 6:
    case 7:
    case 8:
      printf("Thanks!\n");
      break;
    case 9:
    case 10:
    case 11:
    case 12:
      printf("Cool!\n");
      break;

    default:
      printf("*shrug*\n");
      break;
  }
}

void win() {
  printf("\nYou win!\n");
  printf("The flag is: flag{basic-canary}\n");
}
