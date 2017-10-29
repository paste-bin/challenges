#!/usr/bin/python


from Crypto.Cipher import AES
# Encryption
# encryption_suite = AES.new("\x81\xc0\x60\x30\x98\x4c\x26\x93\x49\x24\x92\xc9\x64\xb2\xd9\xec", AES.MODE_CBC, '\x00'*16)
# cipher_text = encryption_suite.encrypt("ABBBBJJJDDDAAAAAAAAA really secret message. Not for prying eyes.")
# print cipher_text
# Decryption

line = "1XNGPhPO4k6Bqi6DQtntQg=="

import base64
cipher = base64.b64decode(line)
with open('words.txt') as wordFile:
    words = wordFile.readlines()
    for word in words:
		word = word.rstrip()
		word = word.lower()
		# print word
		i = 0
		word += '\x00'*(16-len(word))
		decryption_suite = AES.new(word, AES.MODE_CBC,'\x00'*16)
		plain_text = decryption_suite.decrypt(cipher)
		print plain_text




