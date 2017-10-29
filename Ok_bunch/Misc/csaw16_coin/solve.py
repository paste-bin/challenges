#!/usr/bin/python


from pwn import *

def get_num_bills(v,bill):
	num = 0
	while v-bill >= -0.001:
		num += 1
		v -= bill
	return num


conn = remote("misc.chal.csaw.io",8000)
try:
	while True:
		print conn.recvuntil('$')
		val = float(conn.recvuntil('\n').rstrip())

		print val

		moneys = [10000, 5000, 1000, 500, 100, 50, 20, 10, 5, 1, 0.5, 0.25, 0.1, 0.05, 0.01]
		for money in moneys:
			num = get_num_bills(val,money)
			val -= money * num
			print conn.recv()
			print num
			print val
			conn.sendline(str(num))
except:
	pass

conn.interactive()
# $0.07
# $10,000 bills: 1
# $5,000 bills: 1
# $1,000 bills: 1
# $500 bills: 1
# $100 bills: 1
# $50 bills: 1
# $20 bills: 1
# 1$10 bills: 
# $5 bills: 1
# $1 bills: 1
# half-dollars (50c): 1
# quarters (25c): 1
# dimes (10c): 1
# nickels (5c): 1
# pennies (1c): 1






