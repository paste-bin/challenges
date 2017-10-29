#include <stdio.h>
#include <stdlib.h>

/*
 * This is a recreation of the random part 
 * from the boston key party ctf pwn challenge hiddensc
 * - pasteBin 2017
 */

void do_srand(void);
signed long long rand64(void);
int main(int argc, char *argv[]){
	unsigned int v10 = getpagesize(); // 0x1000;
	do_srand();
	unsigned long long randomNum = rand64();
	unsigned long long a;
	unsigned long long d;
	unsigned long long c;
	a = randomNum;
	c = randomNum;
	unsigned long long k = (a - ( ((((a - (( a + (((((a>>10)*0x18001))>>(15*4 - 10))>>3))>>1 ))>>1) + (( a + (((((a>>10)*0x18001))>>(15*4 - 10))>>3))>>1 ))>>46) * 0x555555555555)) & 0xfffffffffffff000;


	d = 0x8000000000018001;
	c = a;
	// multiply a and d and store the high part in d
	// lots of magic later...
	d = ( a + (((((a>>10)*0x18001))>>(15*4 - 10))>>3))>>1 ; //((a*8) + ((((a>>10)*0x18001))>>(15*4 - 10)))>>4;
	a = a - d;
	a >>=1;
	a += d;
	a >>=46;
	d = 0x555555555555;
	a = a * d; //(imul)
	c = c - a ;
	a = c;
	d = 0xfffffffffffff000;
	a = a & d;


	printf("[!] shellcode is at 0x%lx\n", a);
	printf("[!] shellcode is at 0x%lx\n", k);

	return EXIT_SUCCESS;
}


void do_srand(void) {
  unsigned int buf; // [rsp+0h] [rbp-10h]@1
  int fd; // [rsp+4h] [rbp-Ch]@1
  long long v3; // [rsp+8h] [rbp-8h]@1

  fd = open("/dev/urandom", 114);
  read(fd, &buf, 4uLL);
  srand(buf);
  // printf("seeding with %x\n", buf);
}

signed long long rand64(void) {
  signed int i; // [rsp+4h] [rbp-1Ch]@1
  signed long long v2; // [rsp+8h] [rbp-18h]@1

  v2 = 0LL;
  for ( i = 0; i <= 63; ++i )
    v2 = 2 * v2 + rand() % 2;

  // printf("[!] random value is 0x%lx\n", v2);
  return v2;
}



// a = randomNum;
// c = randomNum;
// multiply a and d and store the high part in d
// lots of magic later...
// a = (a - ( ((((a - (( a + (((((a>>10)*0x18001))>>(15*4 - 10))>>3))>>1 ))>>1) + (( a + (((((a>>10)*0x18001))>>(15*4 - 10))>>3))>>1 ))>>46) * 0x555555555555)) & 0xfffffffffffff000;





// im thinking that this is not as simple as it looks in ida

// int rand64() {
//     var_18 = 0x0;
//     for (var_1C = 0x0; var_1C <= 0x3f; var_1C = var_1C + 0x1) {
//             rax = rand();
//             var_18 = sign_extend_32(
//             	(
//             		rax + 
//             		(
//             			SAR(rax, 0x1f) >> 0x1f
//             		) & 0x1
//             	) - 
//             	(
//             		SAR(rax, 0x1f) >> 0x1f
//             	)
//             ) + var_18 + var_18;
//     }
//     rax = var_18;
//     return rax;
// }



/*


rand64 gives 
0x159ea7ba623eb94d
a = c = 0x159ea7ba623eb94d
d = 0x8000000000018001
c = a
d:a = d * a
0xacf53dd311f7d1491363b187832394d
d = 0xacf53dd311f7d14
a = 0x91363b187832394d

a = c
a = 0x159ea7ba623eb94d

so we've saved the overflow (which is small(ish(er))) to rdx at this point

a = a - d
a = 0xacf53dd311f3c39

right shift a right 1 
i.e lop off the last bit
a = 0x567a9ee988f9e1c

a += d
a = 0x1036fdcbc9af1b30

right shift a 46 to the right

a = 0x40db
lolz, leaves us with like 15 bits

d = 0x555555555555


a = a * d (imul)
a = 0x159e555555553fb7

c = c - a 
c = 0x52650ce97996
a = c
a = 0x52650ce97996
d = 0x1000 // page size 
neg d 
d = 0xfffff000
signed extend mov d -> d
d = 0xfffffffffffff000

a = a & d
a = 0x52650ce97000














>>> hex(0x159ea7ba623eb94d * 0x8000000000000000)
'0xacf53dd311f5ca68000000000000000L'
>>> hex(0x159ea7ba623eb94d * 0x0000000000018001)
'           0x206e11363b187832394dL'
>>> hex(0x159ea7ba623eb94d * 0x8000000000018001)
'0xacf53dd311f7d1491363b187832394dL'


0xacf53dd311f5ca68000000000000000L
'          0x206e11363b187832394dL'
0xacf53dd311f7d14



*/

/*
actually calling rand




b = 2*a
a = rand
a = 0x2f578e6c
d = a
d = 0x2f578e6c
a = d

sar    eax,0x1f
shr    eax,0x1f

arithmetic shift right 
logic shift right

so save the sign for the first 31 bits

so we get the left most 2 bits are now the right most
and if the biggest bit is a 1 then the next 31 bits are 1 then 0s else all 0s

a = 0
a = 0

d += a
d = d & 1
d = d - a
a = d

sign extend eax into rax

a += b








*/
