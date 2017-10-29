#!/usr/bin/python

from json import load as loadJSON
from Crypto.Cipher import AES
from sys import stdin, stdout

def pad(blockLen, data):
    padNum = (blockLen - (len(data) % blockLen)) % blockLen
    padding = ""
    for x in xrange(padNum):
        padding += chr(0x00)
    return data + padding

def encrypt(key, flag):
    cipher = AES.new(key)
    stdout.write("Enter in some hexadecimal encoded data and we will encrypt\n\
it for you using a secret key:\n")
    stdout.flush()

    stdin.flush()
    userData = stdin.readline().rstrip().decode('hex')
    stdin.flush()
    plaintext = pad(len(key), "K17LOCKER:" + userData + flag)

    ciphertext = cipher.encrypt(bytes(plaintext))

    stdout.flush()
    stdout.write("Here is your encrypted data:\n")
    stdout.write(ciphertext.encode('hex'))
    stdout.write("\n")
    stdout.flush()

secret = loadJSON(file("secret.json"))

key = bytes(secret["key"].decode("hex"))
flag = bytes(secret["flag"])

while True:
    try:
        encrypt(key, flag)
    except:
        break
