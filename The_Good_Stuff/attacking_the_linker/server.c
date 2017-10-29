#include <stdio.h>
#include <stdlib.h>

#include "funcs.h"

#define FOREVER 1

#define FLAG_LEN 46

unsigned long get_num(char *str);

// Each function messes with a byte of this string
unsigned char buf[FLAG_LEN + 1] =
	"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
void write_what_where(unsigned long *where, unsigned long what) {
	printf("I'm writing 0x%lx to -> 0x%lx\n", what, where);
	fflush(stdout);
	*where = what;
}

void vulnerable_func(void) {
	printf("Enter 0 to exit\n");
	fflush(stdout);

	while (FOREVER) {
		unsigned long index = get_num((char *)"Enter an address (decimal):");

		if (index == 0) {
			break;
		}

		printf("you entered 0x%x\n", index);
		fflush(stdout);
		unsigned long value = get_num((char *)"Enter a value:");
		write_what_where(index, value);
	}
	printf("Exiting \n");
	fflush(stdout);
}

unsigned long get_num(char *str) {
	unsigned long ret = 0;
	printf("%s", str);
	fflush(stdout);
	scanf("%ld", &ret);
	getchar();  // prevent loop
	return ret;
}

int main(int argc, char const *argv[]) {
	printf(
		"Welcome to a crappy program that has a write what where\n"
		"vulnerability. To get the flag you need to exploit this\n"
		"program in such a way as to call the right functions in\n"
		"the right order.\n"
		"Fortunatly we have a solution for you! But it's not very \n"
		"good becasue it uses hardcoded offsets. Reverse engineer \n"
		"the solution and fix it to get the flag\n"
		"\n"
		"Hint: gdb is your friend ;)\n"
		"\n");
	vulnerable_func();
	func0(buf);
	func1(buf);
	func2(buf);
	func3(buf);
	func4(buf);
	func5(buf);
	func6(buf);
	func7(buf);
	func8(buf);
	func9(buf);
	func10(buf);
	func11(buf);
	func12(buf);
	func13(buf);
	func14(buf);
	func15(buf);
	func16(buf);
	func17(buf);
	func18(buf);
	func19(buf);
	func20(buf);
	func21(buf);
	func22(buf);
	func23(buf);
	func24(buf);
	func25(buf);
	func26(buf);
	func27(buf);
	func28(buf);
	func29(buf);
	func30(buf);
	func31(buf);
	func32(buf);
	func33(buf);
	func34(buf);
	func35(buf);
	func36(buf);
	func37(buf);
	func38(buf);
	func39(buf);
	func40(buf);
	func41(buf);
	func42(buf);
	func43(buf);
	func44(buf);
	func45(buf);

	printf("%s\n", buf);
	fflush(stdout);

	return 0;
}
