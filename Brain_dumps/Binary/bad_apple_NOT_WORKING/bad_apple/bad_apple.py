#!/usr/bin/env python3
import sys, binascii
import hashlib
key = open('key.bin', 'rb').read()
sha256 = hashlib.sha256()
message = sys.stdin.buffer.read(0x100)
digestLength = 32
#if len(message) < digestLength:
#  print('len')
#  exit(0)

tag, message = message[:digestLength], message[digestLength:]

print (tag)
print (message)
sha256.update(key + message)
dj = sha256.digest()
print (dj)
if dj != tag:
  print('bad')
  exit(0)

if b'hello pls' in message:
  print('hello')
if b'flag pls' in message:
  print(open('flag.txt', 'r').read())

