/*
 * This is for the FreelancerCTF
 * made by pasteBin 
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define FOREVER 1
#define MAX 256 
#define IS_ADMIN 0
#define NOT_ADMIN 1


void func(void);
int64_t get_num(void);
int get_privs(void);

int main(int argc, char *argv[]){
	
	func();
	return EXIT_SUCCESS;
}

int get_privs(void){
	printf("Are you the admin?\nY/N>");
	fflush(stdout);
	int admin = NOT_ADMIN;
	char resp = getchar();
	if (resp == 89){
		admin = 1;
	}
	return admin;
}

void func(void){
	int privLevel = get_privs();
	int64_t num = get_num();

	if (num >= 256 && privLevel == NOT_ADMIN){ // stop numbers > 256 being entered
		num = num%256;
	}
	if (num*2 == 0xf5ee1a2ce5*2){
		printf("With such skill you must be the admin!\n"
			   "FCTF{REDACTED}\n");
		fflush(stdout);
	}else{
		printf("Haha no flag 4 u\n");
	}
}

int64_t get_num(void){
	int64_t ret = 0;
	printf("Enter a number:");
	fflush(stdout);
	scanf("%lld", &ret);
	getchar(); // prevents an infinite loop, not important
	return ret;
}


