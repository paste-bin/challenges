# Attacking the linker
This is designed as a flexible introduction to linkers 

## How the challenge works
`server.c` calls functions 0-46 e.g 'func0()' from libfuncs which all modify the flag buffer with a random xor. The main program has a 'write what where' vulnerability and there is a broken exploit `exp.py` that exploits this to swap the entries in the got/plt of the functions so that it prints the flag.

## Challenge setup
A precompiled setup is included in `challenge.zip`  
To reacreate this from scratch with a different flag, read on..  
  
`./gen.py`
This python script generates funcs.c and tells you the correct order that the functions need to be called in so that the main program prints the flag.

Once you have generated 'funcs.c' run `make` to compile the main binary and libfuncs.so  

## Solution
Disable ASLR (perhaps by running the program in gdb) and find the address that libfuncs gets loaded in.  
e.g `ldd ./main`  
or
```
gdb ./main
gdb) start
gdb) vmmap
```
This will show where libfuncs.so is mapped in.  
Update the address in the broken exploit to be the correct start of libfuncs and the exploit will now work.  
#### Note
pwntools is required for the exploit to work  


