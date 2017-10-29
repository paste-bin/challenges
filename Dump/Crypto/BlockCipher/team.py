#!/usr/bin/python
from aes_common import *

# team code
# default ecb

# must change
secret = pad("woopiedoopdydoo")
setup(secret)


def encrypt(blocks):
	cipher_blocks = [encode_block(block) for block in blocks]
	return cipher_blocks

def decrypt(cipher_blocks):
	blocks = [decode_block(''.join(cipher_block)) for cipher_block in cipher_blocks]
	return blocks

team = {
	"name" : "team0",
	"code" : "banana",
	"encrypt" : encrypt,
	"decrypt" : decrypt
}