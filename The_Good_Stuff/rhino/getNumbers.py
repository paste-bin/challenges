#!/usr/bin/python
import sys
import array

xor = int(sys.argv[1], 16)
hex_data = sys.argv[2].decode('hex')

# print "showing options for {0}".format(string)

print '****',
for c in xrange(len(bytearray(hex_data)) -1):
	print '____',

print 
for b in bytearray(hex_data):
	res = xor^b
	print hex(res),