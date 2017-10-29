#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from struct import pack, unpack


while True:

	shift = int(raw_input("Shift:"), 16)
	msg = raw_input("Msg:")
	array = []
	for char in msg:
		array.append(str( hex( (int(char, 16)-shift)%16 )[2:]))

	out = ''.join(array)

	print out

	# print conn.recvuntil("\n")
	# print conn.recvuntil("\n")