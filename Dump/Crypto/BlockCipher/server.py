#!/usr/bin/env python

from Crypto.Cipher import AES
import base64
import os
BLOCK_SIZE = 16

# pad with the number of bytes needed to pad as the value PKSC7 or whatevs
# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: c.encrypt(s)
DecodeAES = lambda c, e: c.decrypt(e)

# xor 2 lists
xor = lambda s, t: [chr(ord(a) ^ ord(b)) for a, b in zip(s, t)]

secret = pad("fb5fb99578899228ea9f6c89325cbe") # do not change!

# create a cipher object using the random secret
cipher = AES.new(secret)

def chunks(l, n):
	"""return a list of successive n-sized chunks from l."""
	arr = []
	for i in range(0, len(l), n):
		arr.append(l[i:i+n])
	return arr

def encode(string):
	"""
		encode a string
	"""
	encoded = EncodeAES(cipher, string)
	return encoded

def decode(string):
	"""
		decode the encoded string
	"""
	decoded = DecodeAES(cipher, string)
	return decoded

def cbc_encrypt(string):
	blocks = string
	cipher_blocks = [encode(blocks[0])]
	for prevIndex, block in enumerate(blocks[1:]):
		# do the xor
		pre_encode = xor(cipher_blocks[prevIndex], block)
		cipher_string = [x for x in encode(''.join(pre_encode))]
		# print [x for x in pre_encode2]
		cipher_blocks.append(cipher_string)
	return cipher_blocks

def cbc_decrypt(string):
	cipher_blocks = string
	blocks = [decode(''.join(cipher_blocks[0]))]
	for prevIndex, cipher_string in enumerate(cipher_blocks[1:]):
		pre_encode = [x for x in decode(''.join(cipher_string))]
		# do the xor
		block = xor(pre_encode, cipher_blocks[prevIndex])
		blocks.append(block)

	return blocks

def validate(blocks):
	plainText = ''.join([ ''.join(a) for a in cbc_decrypt(blocks)])
	counter = ord(plainText[-1])
	if counter < 0 or counter > 16:
		return False

	for p in plainText[-counter:]:
		if ord(p) != counter:
			return False
	return True

# cbc_enc = cbc_encrypt(chunks(pad("1234567890123456This is a random cipher text. Nothing special to see here. Congradulations Have a flag jordan{jumpin_beans_and_carrot_fiends}"), BLOCK_SIZE))
# print base64.b64encode(''.join([ ''.join(a) for a in cbc_enc]))
# print validate(cbc_enc)
# print ''.join([ ''.join(a) for a in cbc_decrypt(cbc_enc)])






