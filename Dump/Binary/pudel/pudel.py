#!/usr/bin/env python3
import os, socket, binascii
from Crypto.Cipher import AES

key = open('key.bin', 'rb').read()

lsock = socket.socket()
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind(('', 1043))
lsock.listen(16)

while True:

  sock, addr = lsock.accept()
  print(addr, end = ' ')

  message = sock.recv(0x100)
  if len(message) < 32 or len(message) % 16:
    print('len')
    sock.send(b'len\n')
    continue

  blocks = [message[i : i + 16] for i in range(0, len(message), 16)]

  aes = AES.new(key, AES.MODE_ECB)
  prev_block = blocks[0]
  blocks = blocks[1:]
  message = b''
  for block in blocks:
    message += bytes(x ^ y for x, y in zip(aes.decrypt(block), prev_block))
    prev_block = block

  n = message[-1]
  if n not in range(1, 17) or any(message[-i] != message[-1] for i in range(1, n + 1)):
    print('bad')
    sock.send(b'bad\n')
    sock.close()
    continue
  message = message[:-n]
  print(binascii.hexlify(message).decode())

  sock.send(b'kthx\n')
  sock.close()

