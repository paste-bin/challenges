// Harry J.E Day for SECSOC Freelancer CTF 
// 7/04/2016
// compile: gcc -o badPassword badPassword.c
// A basic password check that will have the password string vissible in the binary

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define STRING_LEN 100
#define FLAG_LEN 23

int main(int argc, char ** argv) {
    
    printf("Please enter the ultra secret password:\n");
    
    char stringBuffer[STRING_LEN];
    fgets(stringBuffer, STRING_LEN, stdin);
    
    if(strncmp(stringBuffer, "flag{youFoundThe$tring}", 23) == 0) {
        printf("Success\n");
    } else {
        printf("Access denied\n");
    }
    return EXIT_SUCCESS;
}