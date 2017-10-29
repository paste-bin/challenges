#!/usr/bin/python

import sys
import base64

cipher = base64.b64decode("5PV1dvnwS33r8nFO+vZmeOz+S2L27HJ3/w==")
key = raw_input(" > ").rstrip()
try:
  key_int = int(key)
except:
  key_int = 0xFF011791
a = "0x%08x" % key_int
b = [0,0,0,0]
b[0] = int(a[2:4],16)
b[1] = int(a[4:6],16)
b[2] = int(a[6:8],16)
b[3] = int(a[8:10],16)
out = ""
for i in range(0,len(cipher)):
  out += chr(ord(cipher[i]) ^ b[i % 4])
print out
