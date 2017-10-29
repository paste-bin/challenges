#include <stdlib.h>
#include <string.h>

// 9447 2015s2
// > exploitation #1
// compile: gcc q1.c -o q1 -m32 

// goal: 
// exploit this program to obtain a shell

void win(void) 
{
    execv("/bin/sh", NULL);
}

int main(int argc, char ** argv) 
{
    char buf[256];

    if (argc != 2)
        exit(-1);

    strcpy(buf, argv[1]);

    return 0;
}
