/*	
 *  This has a printf vuln AND a buffer overflow
 *  talk about chose your own adventure!
 *	Now shut up and smash the stack - pasteBin
 */

#include <stdio.h>
#include <stdlib.h>

void func(void);
void printFlag(void);

int main(int argc, char *argv[]) {
    func();
    return EXIT_SUCCESS;
}

void func(void) {
    char array[100];
    printf("array is at %x\n", &array);
    printf("Hello friend, what is your name\n");
    printf("ENTER NAME> ");

    fflush(stdout);

    scanf("%s",array);
    printf(array);
    fflush(stdout);
}


void printFlag(void){

	FILE *fp;
	char ch[100];
	fp = fopen("./flag.txt", "r");
	fgets(ch, 99, fp);
	fclose(fp);
	printf("The flag is %s", ch);
	fflush(stdout);
}


