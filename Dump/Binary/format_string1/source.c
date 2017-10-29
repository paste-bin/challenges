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
    printf("This should be fun ;)\n");
    printf("Enter your format string:");
    fflush(stdout);
    char array[1000];
    fgets(array, 900, stdin);
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


