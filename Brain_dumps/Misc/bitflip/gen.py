#!/usr/bin/python


from Crypto.Cipher import AES
import sys

def split(s, chunk_size):
    a = zip(*[s[i::chunk_size] for i in range(chunk_size)])
    return [''.join(t) for t in a]


message = 'the idea of this challenge is to change this 7 to an 8. Goodluck'

while len(message)%16 != 0:
	message += '\x00'

# Encryption
key = "goober"
key += "\x00"*(16-len(key))
encryption_suite = AES.new(key, AES.MODE_CBC, '\x00'*16)
cipher_text = encryption_suite.encrypt(message)
# sys.stdout.write(cipher_text)
# print message[29 + 16]
print split(message,16)
print split(message.encode("hex"),16*2)
ciphers = split(cipher_text.encode("hex"),16*2)
xors = ['00'*16]
xors += ciphers[:-1]
print xors
print ciphers
e = cipher_text[29]
e = chr(ord(e) ^ ord('7') ^ ord('H'))
cipher_textArray = split(cipher_text,1)
cipher_textArray[29] = e
cipher_text = ''.join(cipher_textArray)
ciphers = split(cipher_text.encode("hex"),16*2)
# # Decryption
xors = ['00'*16]
xors += ciphers[:-1]
# print xors
enc = cipher_text
# print enc
decryption_suite = AES.new(key, AES.MODE_CBC,'\x00'*16)
plain_text = decryption_suite.decrypt(enc)
print ciphers
print xors
print split(plain_text.encode("hex"),16*2)
print plain_text



