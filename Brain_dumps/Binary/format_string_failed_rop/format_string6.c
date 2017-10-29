/*
 | Easy format string CTF challenge
 | The aim is to write a null to a variable you have the address of
 | compile with 'gcc source.c -o format_string -Wall -m32'
 | by pasteBin for the COMP9447 Security course
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 *	   ____                    __        __      _             *	
 *	  / __/__  ______ _  ___ _/ /_  ____/ /_____(_)__  ___ _   *	
 *	 / _// _ \/ __/  ' \/ _ `/ __/ (_.-/ __/ __/ / _ \/ _ `/   *	
 *	/_/  \___/_/ /_/_/_/\_,_/\__/ /___/__/ _/ /_/_//_/\_, /    *	
 *	                                                 /___/     *	
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

#include <stdio.h>

void do_the_format(void);

int main(int argc, char *argv[]){
	printf(
"___________                          __      _________ __         .__                \n"
"\\_   _____/__________  _____ _____ _/  |_   /   _____//  |________|__| ____    ____  \n"
" |    __)/  _ \\_  __ \\/     \\\\__  \\\\   __\\  \\_____  \\\\   __\\_  __ \\  |/    \\  / ___\\ \n"
" |     \\(  <_> )  | \\/  Y Y  \\/ __ \\|  |    /        \\|  |  |  | \\/  |   |  \\/ /_/  >\n"
" \\___  / \\____/|__|  |__|_|  (____  /__|   /_______  /|__|  |__|  |__|___|  /\\___  / \n"
"     \\/                    \\/     \\/               \\/                     \\//_____/  \n"
"\n"

	);
	printf("Once thought to be just a lazy short cut,\n"
		"actually leads to remote code execution!\n\n"
		"\n"
		"\n"
		"Lets give that a crack shall we?.\n"
		"format string> ");
	fflush(stdout);
	do_the_format();
	return 0;
}

void do_the_format(void){
	char format_string[101];
	fflush(stdout);
	fgets(format_string, 99, stdin);
	format_string[100] = '\0';
	printf(format_string); // I feel dirty typing this
	puts("Having fun?");
	fflush(stdout);
}









