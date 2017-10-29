#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from struct import pack, unpack

conn = remote("randBox-iw8w3ae3.9447.plumbing", 9447) 

while True:

	#opening stuff
	print conn.recvuntil("\n")
	print conn.recvuntil("'")
	msg = conn.recvuntil("'")[:-1]
	print "Message:" + msg
	print conn.recvuntil("\n")
	print conn.recvuntil("\n")

	#send a 0 to get the shift

	conn.sendline('0')

	shift = int(conn.recvuntil("\n"), 16)
	print "Shift :" + str(shift)

	print conn.recvuntil("\n")

	array = []

	for char in msg:
		array.append(str( hex( (int(char, 16)-shift)%16 )[2:]))

	out = ''.join(array)

	print out
	conn.sendline(out)

	conn.interactive()

	# print conn.recvuntil("\n")
	# print conn.recvuntil("\n")