//By: Ricard McGill Grace
//Date: 18/04/2016

//A program which uses XOR encryption to check if the password you 
//inputted is correct

//if you are trying to crack it do not use brute force techniques since
//that will take the fun out of everything :)

//also you have to listen to Megalovania while cracking the password
//because YOU WILL HAVE A BAD TIME...hopefully
//link -> https://www.youtube.com/watch?v=B2jVbSI9H4o

//Copyright: 
//You may use or modify this if:
//1. I give you permission
//2. You give me credit for the original code :)

// Stolen, mostly rewritten, and made insecure (I didn't have to do anything for that part mwahah) 
// by Jordan brown with permission 13/11/16

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#define PASSWORD_LENGTH 32
#define PASSWORD_BUFFER 2
#define BITS_IN_CHAR 8
#define BASE 2

#define FALSE 0
#define TRUE 1

//password constants
#define MESSAGE "you will never guess the pass!!!"
#define RESULT 112,143,224,185,64,224,191,105,148,184,13,124,48,244,179,173,38,172,18,217,112,98,3,72,128,187,240,159,234,136,38,177

void getPassword (char* password);
void clearString (char* string, int length);
int checkPassword(char* password, char* reversePassword);

char reverseByte(char inputChar);

int main (int argr, char * argv[]) {
    int i = 0;
    long incorrectPasswordAttempts = 0; //just for fun :)
    int successfulLogin = FALSE;
    
    while (!successfulLogin) {
        //initialize the string to 0's
        char password[PASSWORD_LENGTH + PASSWORD_BUFFER] = {0};
        
        getPassword(password); 
        
        //initialize reversed password string - REMEMBER THIS IS A REVERSAL ON A BINARY LEVEL 110010 -> 010011
        char reversePassword[PASSWORD_LENGTH + PASSWORD_BUFFER] = {0};
        
        int i = 0;
        while (i < PASSWORD_LENGTH) {
            char inputChar = password[PASSWORD_LENGTH - 1 - i];
            char c = reverseByte(inputChar);
            reversePassword[i] = c;
            i++;
        }
        
        //we now have the reversed password
        //time to do XOR calculations
        successfulLogin= checkPassword(password,reversePassword);
        
        if (successfulLogin) { //Did you guess correctly??????
            printf("\n");
            printf("Welp, you managed to log in...\n");
            printf("You now have admin privileges\n");
            printf(".\n");
            printf("..\n");
            printf("...\n");
            printf("=================== WARNING ===================\n");
            printf("|| Are you sure you wish to delete system32? ||\n");
            printf("===============================================\n");
            printf("Y/N : Y\n");
            printf("\n");
            printf("Deleting...Done\n");
            printf("This program will now exit. Have a nice day.\n");
        } else {
            incorrectPasswordAttempts++;
            if (incorrectPasswordAttempts <= 10) {
                switch (incorrectPasswordAttempts) {
                    case 1: printf("Nope. Try again.\n");
                    break;
                    case 2: printf("Nope. Still Wrong.\n");
                    break;
                    case 3: printf("Third time lucky? I don't think so.\n");
                    break;
                    case 4: printf("Four lives down.\n");
                    break;
                    case 5: printf("Penta failure!\n");
                    break;
                    case 6: printf("Nope. You are still incorrect.\n");
                    break;
                    case 7: printf("This is your lucky 7th guess! You guessed wrong!\n");
                    break;
                    case 8: printf("If you rotate the number 8 by 90 degrees, that's the amount of times you will get the password wrong.\n");
                    break;
                    case 9: printf("9 out of 9 of your guesses are incorrect.\n");
                    break;
                    case 10: printf("You might want to give up now, since you are still incorrect.\n");
                    break;
                }
            } else {
                printf("That expression... thats the expression of someone who has entered a password incorrectly %ld times.\n", incorrectPasswordAttempts);
            }
            printf("\n");
        }
        
    }
    
    return EXIT_SUCCESS;
}


char reverseByte(char inputChar){
    int i = 0;
    char in = inputChar;
    char result = 0;
    for (i = 0; i < BITS_IN_CHAR; ++i){
        int lastBit = 1 & inputChar;
        result |= lastBit;
        if (i + 1 == BITS_IN_CHAR){
            break;
        }
        result = result << 1;
        inputChar >>= 1;
    }
    return result;
}

void getPassword (char* password) { 
    //i dont care what characters you input as long as it is up to 31 chars long
    int validPass;
    
    do { //needs to run code at least once
        validPass = FALSE;
        printf("Please enter a password (31 characters max)\n");
        fgets(password,PASSWORD_LENGTH + PASSWORD_BUFFER,stdin);
        if (password[PASSWORD_LENGTH] == 0) //the pass is correct size (last char should be a null)
        {
            validPass = TRUE;
        } else {
            //clear the buffer and string and try again
            fflush(stdin);
            clearString(password, PASSWORD_LENGTH + PASSWORD_BUFFER);
            printf("The password exceeded 31 characters\n\n");
        }
    } while (!validPass);
} 

void clearString (char* string, int length) { //set everything to null
    int i = 0;
    while (i < length) {
        string[i] = 0;
        i++;
    }
}

int checkPassword(char* password, char* reversePassword) {

    // printf("Pass: %s\n Rev: %s\n", password, reversePassword);
    //do the XOR encryption process to determine if the password is correct
    char message[PASSWORD_LENGTH + PASSWORD_BUFFER] = {0};
    strcpy(message,MESSAGE);
    char result[PASSWORD_LENGTH + PASSWORD_BUFFER] = {RESULT};
    
    int i = 0;
    int correctParts = 0;
    while (i < PASSWORD_LENGTH) {
        if ((message[i] ^ password[i]) == (result[i] ^ reversePassword[i])) {
            correctParts++;
        }
        i++;
    }
    
    int correctPassword = FALSE;
    if (correctParts == PASSWORD_LENGTH) {
        correctPassword = TRUE;
    }
    
    return correctPassword;
}