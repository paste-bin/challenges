/*
 * encryptPrime2.c
 * A program that encrypts a string based on a given seed. 
 * The seed is entered by the user. Any number is a seed!
 * Each character in the string is typecasted to a long,
 * Each letter in the alphabet is given a prime number.
 * This prime number is based on it's place in the alphabet.
 * This begins with A, B, C... for the sake of ASCII.
 * I.e. A = 2, B = 3, C = 5, D = 7, E = 11 ....
 * a = the 27th prime, b = the 28th......
 *
 *
 * This newer version also uses a chain seed to encrypt a string.
 *
 * 
 * Program created by Emmet Murray 27/05/2016
 *
 */


#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#define STOP -1
#define MAX_LOWER 'z'
#define MIN_LOWER 'a'
#define MAX_UPPER 'Z'
#define MIN_UPPER 'A'

unsigned long long encrypt (char letter, unsigned long long *seed);

int main (int argc, char *argv[]) {

   //Creating space for our chain seed

   unsigned long long *seed = malloc(sizeof(unsigned long long));

   *seed = 0;

   unsigned long long encryptedChar;
   int character = 0;

   printf("Please enter your seed: ");
   scanf("%llu", &(*seed));

   printf("Now enter the string you wish to be encrypted: ");

   character = getchar();
   while (character != STOP){

      encryptedChar = encrypt(character, seed);
      printf("%llu", encryptedChar);
      printf(" ");
      character = getchar();

   }
   
   printf("\n");

   // Some housekeeping with variables
   character = 0;
   free(seed);

   return EXIT_SUCCESS;

}

unsigned long long encrypt (char letter, unsigned long long *seed) {

   // This first section grabs the prime number for the ASCII value.

   int upperPrimes[] = {2,3,5,7,11,13,17,19,23,29,31,37,41,43,47
                         ,53,59,61,67,71,73,79,83,89,97,101};

   int lowerPrimes[] = {103,107,109,113,127,131,137,139,149,151
                           ,157,163,167,173,179,181,191,193,197
                           ,199,211,223,227,229,233,239};


   unsigned long long encryptedChar = 0;
   int primeChar = 0;

   // Using the previous value of seed for some computations
   unsigned long long tempSeed = *seed;
   
   if (letter >= MIN_LOWER && letter <= MAX_LOWER) {

      letter = letter - MIN_LOWER;
      primeChar = lowerPrimes[(int) letter];

   } else if (letter >= MIN_UPPER && letter <= MAX_UPPER) {

      letter = letter - MIN_UPPER;
      primeChar = upperPrimes[(int) letter];

   }

   // This part of the code encrypts everything based on the formula.
   // This formula also ensures that the number is positive.
   // The seed is now what is initially in the malloced space for seed.
   //
   // f = 2*seed - 3*seed/100 + 11
   //
   tempSeed = (5*(tempSeed)) - (3*(tempSeed))/100 + 11;

   //printf("%llu\n", seed);
   //printf("%d\n", primeChar);

   encryptedChar = (tempSeed)*primeChar;

   // Assigning the new value for seed back to the malloced area
   *seed = tempSeed;

   //I do this so anyone looking in the memory doesn't steal my stuff :^)
   primeChar = 0;

   //printf("%llu\n", encryptedChar);

   return encryptedChar;
}




