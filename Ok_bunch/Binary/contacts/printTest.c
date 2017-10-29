/* Jordan Brown
 * testing the order of operations of printf
 * 2016
 */

#define T "%1$2c"
#define E T T T T
#define T4 E E E E E E 

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]){
	
	int n = 0x41; //6th place down
	int *p = &n;  //5th
	int **q = &p; //7th

	printf("%66c  %1$c(%2$s) %2$n %1$c(%2$s)\n",*p,p);
	//				A(A)             A(A)
	//				A(A)             L(L)
	//				A(A)             L(A)
	//				A(A)             A(L)

	// printf("%66c  %1$c(%2$s) long%2$n %1$c(%2$s)\n",*p,p);

	// printf("%6$x '%7$s' %n '%7$s' %6$x %7$x\n",p);


	// I need to get a pointer to the stack when printf
	// is called
	// printf("%p %6$x %7$x\n",p);

	// printf("AAAAAAAA%x.%x.%x.%x.%x.%x.%x.%x\n",q);
	printf("%65c(%6$*6$x) '%7$s' %n '%7$s' (%6$*6$x) %7$x\n",p);
	// printf("%65c(%6$*6$x) '%7$s' %n '%7$s' (%6$*6$x) %7$x\n",p);
	// printf("%65c(%6$*6$x) '%7$s' %n '%7$s' (%6$*6$x) %7$x\n",p);
	// printf("%65c(%6$x) '%7$s' %1$n '%7$s' (%6$x) %7$x %2$x\n",p,*p);

	// printf("%65c(%6$x) '%7$s' %1$n '%7$s' (%6$x) %7$x %2$x\n",p);


	// int n = 0x41; //6th place down
	// int *p = &n;  //5th
	// int **q = &p; //7th
	// // printf("%65c (%5$s) '%7$.4s' %5$n %7$n '%7$s'  (%5$s) (%5$x)\n",p);

	// // int n;
	// // printf(T4"AAA%2$n%2$s\n",8,&n);
	// // printf("%2$*1$m",9);
	// printf("%6$x %n %6$x %7$x\n",p);
	// printf("%6$x %n %6$x %7$x\n",p);



	return EXIT_SUCCESS;
}