#!/usr/bin/python

#sender
from pwn import *
context.log_level = 50
key = chr(0xc0)+chr(0xfe)+chr(0xba)+chr(0xbe)+chr(0x3b)+chr(0x30)

for i in range(255):
	conn = remote("35.163.169.111",1337)
	conn.send(chr(i)*(5))
	print i
	print conn.recvall()







