#include <stdio.h>
#include <stdlib.h>

void setup();
void printArray(int array[]);
void thank();
void win();

char *flags[5];

int main(int argc, char *argv[]) {

  setup();

  int secret = 5;
  int array[10] = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3};
  int num;
  
  printf("How many numbers would you like to scan in? ");
  scanf("%d", &num); 

  for (int i=0; i<num; i++) {
    printf("Enter a number: ");
    scanf("%d", &array[i]);
    thank();
  }

  printArray(array);

  if (secret == 0x41414141) {
    win();
  }

  return 0;
}

void printArray(int array[]) {
  printf("The array contains:\n");
  for (int i=0; i<10; i++) {
    printf("%d ", array[i]);
  }
  printf("\n");
}

void setup() {
  // irrelevant
}

char *whichFlag() {
  // irrelevant
}

void thank() {
  // irrelevant
}

void win() {
  printf("You win!\n");
  printf("The flag is: [REDACTED]}\n");
}
