#!/usr/bin/python

import sys

msg = "you will never guess the pass!!!"
res = [112,143,224,185,64,224,191,105,148,184,13,124,48,244,179,173,38,172,18,217,112,98,3,72,128,187,240,159,234,136,38,177]

fd = ''
rd = ''
for x in range(len(msg)):
	thing = str(bin(ord(msg[x]) ^ res[x])[2:])
	while len(thing) < 8:
		thing = str('0') + thing

	fd += thing
	rd = thing[::-1] + rd


# fd == rd
# print fd
# print rd[:128]
solve = fd[:128] + "0"*128
# print
# print solve
# convert solve to data

# def swap(binary, pos):
# 	tmp = binary[pos]
	

chunks = ['']
index = 0
counter = 0
while len(solve) > 0:
	chunks[index] += solve[0]
	counter += 1
	if counter%8 == 0:
		index += 1
		chunks.append('')
	solve = solve[1:]
# print chunks
for chunk in chunks[:-1]:
	num = int(chunk, 2)
	sys.stdout.write(chr(num))











