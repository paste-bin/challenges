#!/usr/bin/python

from Crypto.Cipher import AES
BLOCK_SIZE = 16

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: c.encrypt(s)
DecodeAES = lambda c, e: c.decrypt(e)

# pad with the number of bytes needed to pad as the value PKSC7 or whatevs
# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

# xor 2 lists
xor = lambda s, t: [chr(ord(a) ^ ord(b)) for a, b in zip(s, t)]
secret = pad("woopiedoopdydoo")
cipher = AES.new(secret)


def setup(secret):
	global cipher
	# create a cipher object using the random secret
	cipher = AES.new(secret)


def encode_block(block):
	"""
		encode a block
	"""
	encoded = EncodeAES(cipher, block)
	return encoded

def decode_block(block):
	"""
		decode the encoded block
	"""
	decoded = DecodeAES(cipher, block)
	return decoded



def chunks(l, n):
	"""return a list of successive n-sized chunks from l."""
	arr = []
	for i in range(0, len(l), n):
		arr.append(l[i:i+n])
	return arr

