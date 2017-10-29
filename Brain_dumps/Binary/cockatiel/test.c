#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]){
	
	char *dum;
	unsigned int joe = (unsigned int)strtol(argv[1], &dum, 0);
	printf("%u\n", joe);
	
	return EXIT_SUCCESS;
}
