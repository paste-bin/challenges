#!/usr/bin/python
import sys
import array

def func(a):
	return (4*a + 0x84)%256

hex_data = sys.argv[1].decode('hex')

xor = func(bytearray(hex_data)[0])


# xor = func(bytearray(data)[0])
# hex_data = data[1:]
print ' '.join([hex(x) for x in bytearray(hex_data)])
print "func[{0:<4}] ^ {1}  == {2}".format(hex(bytearray(hex_data)[0]), hex(xor), hex(bytearray(hex_data)[0] ^ xor))


while len(bytearray(hex_data)) > 0:
	
	# print 
	data = []
	for b in bytearray(hex_data):
		res = xor^b
		data.append(res)
		print hex(res),
	print

	xor = func(bytearray(data)[0])
	hex_data = data[1:]
	print
	print "func[{0:<4}] ^ {1}  == {2}".format(hex(bytearray(data)[0]), hex(xor), hex(bytearray(data)[0] ^ xor))

