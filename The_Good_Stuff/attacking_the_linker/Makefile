make_chall:
	gcc -c -Wall -Werror -fpic ./funcs.c
	gcc -shared -o libfuncs.so funcs.o
	gcc -L. -Wl,-rpath=. -Wall -o main server.c -lfuncs 


