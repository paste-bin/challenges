#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// 9447 2015s2
// > exploitation #2
// compile: gcc q2.c -o q2 -m32

// goal: 
// write a ROP exploit for this program
// you may find the leaked address of the payload buffer useful
// after setting up the stack, provide an address to jump to

// warning: this has a non-executable stack! 
//          you DO NOT need shellcode.

// note: you also don't need ROPGadget - objdump works fine here.
//       e.g. % objdump -D q2 | grep <what_you_need>

void fail(void) {
    system("/bin/echo 'wtf?...'");
}

int main(int argc, char ** argv) 
{
    setbuf(stdout, NULL);
    int rop = 0;
    char buf[512] = {0};
    
    printf("leak: %p\n", buf);

    printf("enter buf data: ");
    fgets(buf, sizeof(buf), stdin);

    printf("enter jump addr (in hex): ");
    scanf("%x", &rop);
    
    printf("good luck!\n", rop);
    (*(void(*)()) rop)();

    return 0;
}
