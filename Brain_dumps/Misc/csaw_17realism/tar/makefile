all: as.as link.ld
	yasm -f elf32 as.as -o as.o
	ld -m elf_i386 -o 32.bin -T link.ld as.o
