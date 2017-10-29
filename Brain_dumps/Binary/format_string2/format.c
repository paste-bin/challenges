/*
 | Easy format string CTF challenge
 | The aim is to write a null to a variable you have the address of
 | compile with 'gcc format.c -o run -s -Os -fdata-sections -Wl,--gc-sections -mpreferred-stack-boundary=4 -fno-unwind-tables -fno-asynchronous-unwind-tables -fno-unroll-loops -Wl,-z,norelro -D_FORTIFY_SOURCE=0 -fno-pie -Wno-format -Wno-format-security -fno-stack-protector
'
 | by pasteBin
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

#include <stdio.h>
#include <stdlib.h>
//#include <ctype.h>
#include <string.h>
//#include <signal.h>
//#include <unistd.h>

void do_the_format(void);

int main(int argc, char *argv[]){
	fflush(stdout);
	do_the_format();
	return EXIT_SUCCESS;
}

void do_the_format(void){
	char format_string[0x80];
	char buf[0x80];
	unsigned char change_this = 0x80;
	unsigned char * prt;
	prt = &change_this;
	printf("Welcome Hackers!\nEnter your name:\n>");
	fflush(stdout);
	fgets(buf, *prt -1, stdin);
	sprintf(format_string, "You entered %s", buf);
	fprintf(stdout, format_string);
	format_string[100] = '\0';
	fflush(stdout);
	if (change_this == 0x00){
		printf("FCTF{rock_snakes_eat_small_rakes}\n");
	}
	fflush(stdout);
}

