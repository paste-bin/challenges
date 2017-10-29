// Original code By: Ricard McGill Grace
// Date: 23/3/2016
// A simple program for managing data in an array

// This has been modified to be insecure for the purpose of the Freelancer CTF

#include <stdio.h>
#include <stdlib.h>
//#include <assert.h>
//#include <math.h>
#include <string.h>

#define STRING_LENGTH 256
#define NUMBER_LENGTH 8 //should just be under int max

#define STRCOMP_SUCCESS 0

#define COM_ERROR 0
#define COM_EXIT 1
#define COM_NEW 2
#define COM_GET 3
#define COM_DEL 4
#define COM_SET 5
#define COM_HELP 6
#define COM_SHOW 7

#define TRUE 1
#define FALSE 0
#define NUM_ONLY 2

#define INVALID_VALUE -1

#define MAX_ARRAY_SIZE 1024

/*****************************************
MAKE SURE YOU DELETE ALL UNNEEDED COMMENTS
*****************************************/

void newCommand (void);
void clearString (char* string);
int validCharacter (char character); 
int determineCommand (char* command);
void printHelp (void);
int validCommandString (char* inputString);
void commandNew (int* arraySize, int* createNewPrevValue, int* createNew, int newSize, int* dataArray, int arg1Valid, int arg2Valid);
void commandDel (int* dataArray);
void commandSet (int newData, int position, int arg1Valid, int arg2Valid, int* dataArray, int arraySize);
void commandGet (int position, int arg1Valid, int arg2Valid, int* dataArray, int arraySize);
void commandShow (int arg1Valid, int arg2Valid, int* dataArray, int arraySize);

int main (int argr, char ** argv) {
   
   //only run once (program start up)
   char inputString[STRING_LENGTH] = "";
   char commandString[STRING_LENGTH] = "";
   char number1String[STRING_LENGTH] = "";
   char number2String[STRING_LENGTH] = "";
   int stopProgram = FALSE;
   int commandNumber = COM_ERROR;
   int spacePos1 = INVALID_VALUE;
   int spacePos2 = INVALID_VALUE;
   int commandArg1 = INVALID_VALUE;
   int commandArg2 = INVALID_VALUE;
   int validNum1 = FALSE;
   int validNum2 = FALSE;
   int validInput = FALSE;
   
   //for the new array function
   int createNew = FALSE;
   int createNewPrevValue = 0;
   
   int dataArray[MAX_ARRAY_SIZE];
   int arraySize = 0;
   
   if (commandArg1 == commandArg2) {
      
   }
   
   printf("Welcome the the array program\n");
   fflush(stdout);
   printf("Please type a command or type 'help'\n");
   fflush(stdout);
   
   //run while the user does not exit
   while (stopProgram == FALSE) {
      clearString(inputString);
      clearString(commandString);
      clearString(number1String);
      clearString(number2String);
      
      validInput = FALSE;
      spacePos1 = INVALID_VALUE;
      spacePos2 = INVALID_VALUE;
      validNum1 = FALSE;
      validNum2 = FALSE;
      
      //get input
      newCommand();
      fgets(inputString,STRING_LENGTH - 1,stdin);
      //printf("%s\n", inputString);
      fflush(stdout);
      inputString[strlen(inputString) - 1] = '\0';
      
      //check for valid input
      //check if input uses correct characters
      validInput = validCommandString(inputString);
      if (validInput == FALSE) {
         strcpy(commandString, "INVALID CHARACTERS");
      }
      
      if (validInput == TRUE) { //no anvalit characters
         //find position of spaces
         int c;
         for (c = 0; c < strlen(inputString); c++) {
            if (inputString[c] == ' ') {
               if (spacePos1 == INVALID_VALUE) {
                  spacePos1 = c;
               } else if (spacePos2 == INVALID_VALUE) {
                  spacePos2 = c;
               } else { //too many spaces, throw error
                  strcpy(commandString, "TOO MANY ARGUMENTS");
                  validInput = FALSE;
                  break;
               }
            }
         }
         
         //ensure position of spaces is correct
         if (spacePos1 == 0) {//cannot have space in first position
            validInput = FALSE;
            strcpy(commandString, "FORMATING ERROR");
         } else if (spacePos2 == spacePos1 + 1) {//two spaces in a row
            validInput = FALSE;
            strcpy(commandString, "FORMATING ERROR");
         } else if (spacePos1 == strlen(inputString) - 1 || spacePos2 == strlen(inputString) - 1) {//spaces at end of command or no command
            validInput = FALSE;
            strcpy(commandString, "FORMATTING ERROR");
         }
      }
      
      if (validInput == TRUE) {//the input is valid, process input
         if (spacePos1 == INVALID_VALUE) {//command without arguments
            strcpy(commandString, inputString); //copy into result
         } else {
            int n;
            for (n = 0; n < spacePos1; n++) { //copy command string
               commandString[n] = inputString[n];
            }
            if (spacePos2 != INVALID_VALUE){ //two arguments
               //copy numbers into appropriate number strings
               //int n = spacePos1 + 1;
               for (n = spacePos1 + 1; n < spacePos2; n++) {//copy arg1
                  number1String[n - spacePos1 - 1] = inputString[n];
               }
               for (n = spacePos2 + 1; n < strlen(inputString); n++) {//copy arg2
                  number2String[n - spacePos2 - 1] = inputString[n];
               }            
            } else if (spacePos1 != INVALID_VALUE) {//only 1 arg
               for (n = spacePos1 + 1; n < strlen(inputString); n++) {//copy arg1
                  number1String[n - spacePos1 - 1] = inputString[n];
                  //printf("added num\n");
                  fflush(stdout);
               }
            }
            
         }
         //collection of inputs completed, check to ensure args are numbers
         if (spacePos1 != INVALID_VALUE) {
            
            int t;
            for (t = 0; t < strlen(number1String); t++) {
               if (validCharacter(number1String[t]) != NUM_ONLY) {
                  break;
               }
            }
            if (t == strlen(number1String)) {//completed loop, valid
               validNum1 = TRUE;
            } else {
               strcpy(commandString, "BAD ARGUMENT 1");
            }
               
            
         }
         
         if (spacePos2 != INVALID_VALUE) {
            if (strlen(number2String) <= NUMBER_LENGTH) { //prevent overflow
               int l;
               for (l = 0; l < strlen(number2String); l++) {
                  if (validCharacter(number2String[l]) != NUM_ONLY) {
                     break;
                  }
               }
               if (l == strlen(number2String)) {//completed loop, valid
                  validNum2 = TRUE;
               } else {
                  strcpy(commandString, "BAD ARGUMENT 2");
               }
            } else {
               strcpy(commandString, "BAD ARGUMENT 2");
            }
         }
         
         //if the arg number is valid, convert it to number
         char* resultText;
         if (validNum1 == TRUE) {
            commandArg1 = (int) strtoll(number1String, &resultText, 10);
         }
         if (validNum2 == TRUE) {
            commandArg2 = (int) strtoll(number2String, &resultText, 10);
         }
         
         /*
         //get characters in string
         int i = 0;
         for (i;i < )
         //split this up into 3 processing functions
         //command arg1 arg2
         //check amount of spaces to determine amount of arguments
         //process inpput based on amount of spaces and position of spaces?
         //process input to find command
         int i;
         for (i = 0; i < strlen(inputString); i++) 
         {         
            if (validCharacter(inputString[i]) == TRUE) 
            {
               commandString[i] = inputString[i];
            } 
            else if (inputString[i] == ' ') 
            { 
               //a space has been encountered, possible second argument
               i++; //skip the space, continue processing extra arguments 
               //for each remaining character, determine if number
               int j = 0;
               for (j = i; j < strlen(inputString); j++) 
               {
                  if (j - i < NUMBER_LENGTH) {//no over flow errors
                     if (validCharacter(inputString[j]) == NUM_ONLY) 
                     {
                        number1String[j-i] = inputString[j];
                     } 
                     else if (inputString[j] == ' ') 
                     {
                     //another space encountered, possible third argument
                        j++;
                        int k = 0;
                        for (k = j; k < strlen(inputString); k++)
                        {
                           if (k - j < NUMBER_LENGTH) //no over flow
                           {
                              if (validCharacter(inputString[k]) == NUM_ONLY)
                              {
                                 number2String[k - j] = inputString[k];
                              }
                              else
                              {
                                 break;
                              }
                           }
                           else
                           {//number exceede maximum
                              strcpy(commandString,"BAD THIRD ARGUMENT");
                           }
                        }
                      
                     }
                  } 
                  else 
                  { //number exceded maximum, throw error
                     strcpy(commandString,"BAD SECOND ARGUMENT");
                  }
               }
               
               //convert from string to number (if possible)
               printf("%s\n", number1String);
               fflush(stdout);
               printf("%s\n", number2String);
               fflush(stdout);
               
               
               break;
               
            } else { //Completely invalid data, exit loop
               break;
            }
         }
         //printf("input: %s, Output: %s\n", inputString, commandString);
         fflush(stdout);
         */
         
      } else {
        //strcpy(commandString,"INVALID CHARACTERS");
      }
      
      //determine command code
      commandNumber = determineCommand(commandString);
      
      //execute command
      switch (commandNumber) {
         case COM_NEW: //printf("Creating new array\n");
         fflush(stdout);
         commandNew(&arraySize, &createNewPrevValue, &createNew, commandArg1, dataArray, validNum1, validNum2);
         break;
         
         case COM_GET: //printf("Getting data\n");
         fflush(stdout);
         commandGet (commandArg1, validNum1, validNum2, dataArray, arraySize);
         break;
         
         case COM_DEL: //printf("Deleting data\n");
         fflush(stdout);
         commandDel(dataArray);
         break;
         
         case COM_ERROR: 
         printf("<ERROR> INVALID COMMAND '%s'\n",commandString);
         fflush(stdout);
         break;
         
         case COM_EXIT: printf("Exiting Program\n");
         fflush(stdout);
         stopProgram = TRUE;
         break;
         
         case COM_HELP: printHelp();
         break;
         
         case COM_SET: //printf("Setting data\n");
         fflush(stdout);
         commandSet(commandArg2, commandArg1, validNum1, validNum2, dataArray, arraySize);
         break;
         
         case COM_SHOW: //printf("Showing all data\n");
         fflush(stdout);
         commandShow (validNum1, validNum2, dataArray, arraySize);
         break;
      }
   }
   
   return EXIT_SUCCESS;
}

void newCommand (void) {
   //prints out the symbol signifying user input
   printf(">> ");
   fflush(stdout);
}

void clearString (char* string) { 
   //sets the chars of array to string terminator
   int i;
   for (i = 0; i< STRING_LENGTH; i++) {
      string[i] = '\0';
   }
}

int validCharacter (char character) {
   //check to see if the character inputted is valid
   int valid = FALSE;
   
   if ((character >= 'a' && character <= 'z') || character == ' ') {
      valid = TRUE;
   } else if (character >= '0' && character <= '9') {
      valid = NUM_ONLY;
   }
    
   return valid;
}

int determineCommand (char* command) {
   //determine command inputted based on string
   int comNum = COM_ERROR;
   
   if (strcmp(command, "exit") == STRCOMP_SUCCESS) {
      comNum = COM_EXIT;
   } else if (strcmp(command, "new") == STRCOMP_SUCCESS) {
      comNum = COM_NEW;
   } else if (strcmp(command, "get") == STRCOMP_SUCCESS) {
      comNum = COM_GET;
   } else if (strcmp(command, "del") == STRCOMP_SUCCESS) {
      comNum = COM_DEL;
   } else if (strcmp(command, "set") == STRCOMP_SUCCESS) {
      comNum = COM_SET;
   } else if (strcmp(command, "help") == STRCOMP_SUCCESS) {
      comNum = COM_HELP;
   } else if (strcmp(command, "show") == STRCOMP_SUCCESS) {
      comNum = COM_SHOW;
   }
   
   return comNum;
}

void printHelp (void) {
   printf("==============   Array Program Help Data   ==============\n");
   fflush(stdout);
   printf("Command Syntax        | Description\n");
   fflush(stdout);
   printf("new <length>          | Create array of <length> size\n");
   fflush(stdout);
   printf("get <location>        | Prints data stored at <location\n");
   fflush(stdout);
   printf("show                  | Prints all data stored\n");
   fflush(stdout);
   printf("del <location>        | Resets data at <location> to NULL\n");
   fflush(stdout);
   printf("set <location> <data> | Sets data at <location> to <data>\n");
   fflush(stdout);
   printf("exit                  | Closes program and discards data\n");
   fflush(stdout);
   printf("====================   END OF HELP   ====================\n");
   fflush(stdout);
}

int validCommandString (char* inputString) {
   int valid = TRUE;
   int i;
   for (i = 0; i< strlen(inputString); i++) {
      if (validCharacter(inputString[i]) == FALSE) 
         valid = FALSE;
         fflush(stdout);
         break;
      }
   
   return valid;
}

void commandNew (int* arraySize, int* createNewPrevValue, int* createNew, int newSize, int* dataArray, int arg1Valid, int arg2Valid) {
   if (arg1Valid == TRUE && arg2Valid != TRUE) {
      if (*arraySize == 0 && newSize > 0 && newSize <= MAX_ARRAY_SIZE) {
         *arraySize = newSize;
         printf("Sussessfully created new array of length %d\n", newSize);
         fflush(stdout);
      } else if (newSize > 0 && newSize <= MAX_ARRAY_SIZE) {
         if (*createNew == TRUE && *createNewPrevValue == newSize)
         {
            *arraySize = *createNewPrevValue;
            *createNew = FALSE;
            commandDel(dataArray);
            printf("Resized array to length %d\n", *createNewPrevValue);
            fflush(stdout);
            
         } else {
            printf("This will resize the array to length %d and clear all data in the array\n", newSize);
            fflush(stdout);
            printf("To confirm, input command again\n");
            fflush(stdout);
            *createNewPrevValue = newSize;
            *createNew = TRUE;
         }
      } else {
         printf("<ERROR> ARRAY SIZE OUT OF BOUNDS (MAX IS 1024)\n");
         fflush(stdout);
      }
   } else {
      printf("<ERROR> THE COMMAND 'new' REQUIRES 1 ARGUMENT\n");
      fflush(stdout);
   }
}

void commandDel (int* dataArray) {
   int i;
   for (i = 0; i< MAX_ARRAY_SIZE; i++)
   {
      dataArray[i] = 0;
   }
   printf("Array cleared\n");
   fflush(stdout);
}

void commandSet (int newData, int position, int arg1Valid, int arg2Valid, int* dataArray, int arraySize) {
   if (arg1Valid == TRUE && arg2Valid == TRUE) {
      if (position < arraySize && position >= 0) {
         dataArray[position] = newData;
         printf("Position %d set to %d\n", position, newData);
         fflush(stdout);
      } else {
         if (arraySize == 0) {
            printf("<ERROR> USE THE 'new' COMMAND TO INITIALISE A NEW ARRAY\n");
            fflush(stdout);
         } else {
            printf("<ERROR> POSITION %d IS OUT OF BOUNDS (MAX IS %d)\n", position, arraySize);
            fflush(stdout);
         }
      }
   } else {
      printf("<ERROR> THE COMMAND 'set' REQUIRES 2 ARGUMENTS\n");
      fflush(stdout);
   }
}

void commandGet (int position, int arg1Valid, int arg2Valid, int* dataArray, int arraySize) {
   if (arg1Valid == TRUE && arg2Valid == FALSE) {
      if (position < arraySize) {
         printf("pos [%d] = %d\n", position, dataArray[position]);
         fflush(stdout);
      } else {
         if (arraySize == 0) {
            printf("<ERROR> USE THE 'new' COMMAND TO INITIALISE A NEW ARRAY\n");
            fflush(stdout);
         } else {
            printf("<ERROR> POSITION %d IS OUT OF BOUNDS (MAX IS %d)\n", position, arraySize);
            fflush(stdout);
         }
      }
   } else {
      printf("<ERROR> THE COMMAND 'get' REQUIRES 1 ARGUMENT\n");
      fflush(stdout);
   }
}

void commandShow (int arg1Valid, int arg2Valid, int* dataArray, int arraySize) {
   if (arg1Valid == FALSE && arg2Valid == FALSE) {
      if (arraySize > 0) {
         int i;
         for (i = 0; i < arraySize; i++) {
            printf("[%d] = %d, ", i, dataArray[i]);
            fflush(stdout);
         }
      } else {
         printf("<ERROR> USE THE 'new' COMMAND TO INITIALISE A NEW ARRAY\n");
         fflush(stdout);
      }
      printf("\nEND OF ARRAY\n");
      fflush(stdout);
   } else {
      printf("<ERROR> THE COMMAND 'show' REQUIRES 0 ARGUMENTS\n");
      fflush(stdout);
   }
}