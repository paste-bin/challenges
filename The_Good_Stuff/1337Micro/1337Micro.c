/*
 * This is the 1337 Microprocessor 
 * Write program code to exploit the microprocessor
 * by pasteBin 
 */



#include <stdio.h>
#include <stdlib.h>

#define TAPE_LEN 100
#define LEET 133

#define RED  "\033[91m"
#define GREEN  "\033[92m"
#define BLUE "\033[0;94m"
#define GREY "\033[0;97m"
#define YELLOW  "\033[93m"
#define PINK  "\033[95m"
#define LIGHT_RED "\033[1;31m"
#define LIGHT_BLUE "\033[0;96m"
#define LIGHT_PINK  "\033[94m"
#define END  "\033[0m"

#define LEETMAGIC 0xaa
#define TRUE 1
#define FALSE 0

void quit(unsigned char *ptr);
void inc_reg_1(unsigned char *ptr);
void dec_reg_1(unsigned char *ptr);
void inc_reg_2(unsigned char *ptr);
void dec_reg_2(unsigned char *ptr);
void set(unsigned char *ptr);
void set_word(unsigned char *ptr);
void get(unsigned char *ptr);
void get_word(unsigned char *ptr);
void load_r1(unsigned char *ptr);
void load_r1_word(unsigned char *ptr);
void print(unsigned char *ptr);
void swap(unsigned char *ptr);
void je(unsigned char *ptr);
void jz(unsigned char *ptr);
void jmp(unsigned char *ptr);
void add(unsigned char *ptr);
void printEasyFlag(unsigned char *ptr);


void printTape(void);
int leetCheck(void);

int r1;
int r2;
int ip;
char leet_field[LEET];

char leet_canary;


unsigned char tape[TAPE_LEN+1];
void (*funcs[18])(unsigned char *ptr) = {quit, inc_reg_1, dec_reg_1, inc_reg_2, dec_reg_2, set, set_word, get, get_word, load_r1, load_r1_word, print, swap, je, jz, jmp, add, printEasyFlag};
void init_leet(void);

int main(int argc, char *argv[]){
	ip = 0;
	r1 = 0;
	r2 = 0;
	init_leet();

	printf("Enter Program Bytes\n");
	read(0, tape, TAPE_LEN);
	printTape();
	while(TRUE){
		if (tape[ip] < 0 || tape[ip] >=18){
			printf("INVALID 1337 CODE\n");
			return EXIT_FAILURE;
		}
		funcs[tape[ip++]](tape + r1);
		printTape();
	}

	return EXIT_SUCCESS;
}

void init_leet(void){
	int i;
	for (i = 0; i < LEET; ++i){
		leet_field[i] = 1;
	}
	// set random spot to a 7 aka LEETMAGIC
	srand(time(NULL));
	leet_canary = rand()%255;
	int spot = rand()%LEET;
	int spot2 = rand()%LEET;
	while (spot2 == spot){
		spot2 = rand()%LEET;
	}
	while (leet_canary == 7){
		spot2 = rand()%LEET;
	}

	leet_field[spot] = LEETMAGIC;
	leet_field[spot2] = leet_canary;
}
// Exit with status code tape[ip]
void quit(unsigned char *ptr){
	exit((int)*ptr);
}
void inc_reg_1(unsigned char *ptr){
	r1 += 1;
}
void dec_reg_1(unsigned char *ptr){
	r1 -= 1;
}
void inc_reg_2(unsigned char *ptr){
	r2 += 1;
}
void dec_reg_2(unsigned char *ptr){
	r2 -= 1;
}
void set(unsigned char *ptr){
	*ptr = r2;
}
void set_word(unsigned char *ptr){
	unsigned int *n = (unsigned int *)ptr;
	*n = r2;
}
void get(unsigned char *ptr){
	r2 = *ptr;
}
void get_word(unsigned char *ptr){
	unsigned int *n = (unsigned int *)ptr;
	r2 = *n;
}
void load_r1(unsigned char *ptr){
	r1 = *(tape + ip++);
}
void load_r1_word(unsigned char *ptr){

	if (leetCheck() == TRUE){
		unsigned int *n = (unsigned int *)(tape + ip);
		ip += 4;
		r1 = *n;
	}else{
		printf("Only leet users get to use this function\n");
	}
}
void print(unsigned char *ptr){
	printf("%s\n", ptr); 
}
void swap(unsigned char *ptr){
	int tmp = r1;
	r1 = r2;
	r2 = tmp;
}
void je(unsigned char *ptr){
	if (r2 == r1){
		ip = *(tape + ip);
	}else{
		ip++;
	}
}
void jz(unsigned char *ptr){
	if (r2 == 0){
		ip = *(tape + ip);
	}else{
		ip++;
	}
}
void jmp(unsigned char *ptr){
	ip = *(tape + ip );
}

void add(unsigned char *ptr){
	if (leetCheck() == TRUE){
		r1 = r1 + r2;
	}else{
		printf("Only leet users get to use this function\n");
	}
}


void printEasyFlag(unsigned char *ptr){
	if (leetCheck() == TRUE){
		printf("FLAG\n");
	}
}
int leetCheck(void){
	int is_leet = 0;
	int i;
	int saw_leet_canary = 0;
	for (i = 0; i < LEET; ++i) {
		if (leet_field[i] == 3 && is_leet == 0){
			is_leet = 1;
			printf("lookin Leet!\n");
		}else if(leet_field[i] == 3 && is_leet == 1){
			is_leet = 0;
			printf("HAHAH hack harder!\n");
			return FALSE;
		}else if (leet_field[i] == LEETMAGIC){
			printf("Not leet enought for the 1 double-3 7 Micro ;)\n");
			return FALSE;
		}else if(leet_field[i] == leet_canary){
			saw_leet_canary = TRUE;
			printf("Saw the canary!\n");
		}

	}
	if (is_leet == 1 && saw_leet_canary) {
		return TRUE;
	}else{
		printf("*pffft* it's not that easy!\n");
		return FALSE;
	}
}

void printTape(void){
	printf("TAPE:\n");
	int i = 0;
	for (i = 0; i < TAPE_LEN; ++i){
		if (i == ip){	
			printf(YELLOW);
		}else if(tape[i] == 0){
			printf(GREY);
		}else if(tape[i] >0 && tape[i] < 5){
			printf(GREEN);
		}else if(tape[i] >=5 && tape[i] < 9){
			printf(BLUE);
		}else if(tape[i] >=9 && tape[i] < 11){
			printf(PINK);
		}else if(tape[i] == 11){
			printf(RED);
		}else if(tape[i] == 12){
			printf(LIGHT_PINK);
		}else if(tape[i] >=13 && tape[i] < 16){
			printf(GREY);
		}else if(tape[i] == 16){
			printf(LIGHT_RED);
		}else {
			printf(LIGHT_BLUE);
		}
		printf("%02x: %02hhx " END, i, tape[i]);
		printf("\t");
	}
	printf("R1: %x, R2: %x, IP: %x\n", r1, r2, ip);
}




