import gdb
import sys

def dump(obj):
  for attr in dir(obj):
	print "obj.%s = %s" % (attr, getattr(obj, attr))

def getch():
	import sys, tty, termios 
	fd = sys.stdin.fileno( )
	# old_settings = termios.tcgetattr(fd)
	try:
		# tty.setraw(fd)
		tty.setcbreak(fd)
		ch = sys.stdin.read(1)
	finally:
		pass
		# termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch


RED = '\033[91m'
GREEN = '\033[92m'
BLUE="\033[0;94m"
GREY="\033[0;97m"
YELLOW = '\033[93m'
PINK = '\033[95m'
LIGHT_RED ="\033[1;31m"
LIGHT_BLUE="\033[0;96m"
LIGHT_PINK = '\033[94m'
END = '\033[0m'
CLEAR = '\033[2J'
HIDE = '\033[?25l'


class dumpBreak (gdb.Command):
	"""Greet the whole world."""

	def print_blue(self, difs):
		# original in blue
		for c1, c2 in difs:
			if c1 == c2:
				sys.stdout.write(c1)
			else:
				sys.stdout.write( BLUE +c1+ END)


	def print_red(self, difs):
		# change in red
		for c1, c2 in difs:
			if c1 == c2:
				sys.stdout.write(c1)
			else:
				sys.stdout.write( RED +c2+ END)

	def stop_handler(self, event):
		if "breakpoint" in dir(event) and event.breakpoint.location == self.location:
			dump1 = gdb.execute("x/100wx " + self.mem,to_string=True)
			gdb.execute("ni",to_string=True)
			dump2 = gdb.execute("x/100wx " + self.mem,to_string=True)
	 	
	 		difs = zip([c1 for c1 in dump1], [c2 for c2 in dump2])
	 		change = False
	 		for a, b in difs:
	 			if a != b :
	 				change = True
	 				break

	 		self.print_blue(difs)
	 		up = lambda u: sys.stdout.write("\033[{u}A".format(u=u))# +2 for toggle instruction

 			if change:
	 			print "Toggle "+BLUE+"LEFT"+END+" for before or "+RED+"RIGHT"+END+" for after"
	 			print "Hit return to stop"
	 			up(2)
		 		while True:
		 			ch = getch().encode('hex')
		 			if ch == "1b" and getch().encode('hex') == "5b": 
						ch = getch().encode('hex')
		 				if ch == "44":
							up(25) # start of n lines up
							self.print_blue(difs)

			 			elif ch == "43": # right
							up(25) # start of n lines up
							self.print_red(difs)
					elif ch in ["0d", "0a"]:
						break
					else:
						print ch

		return	 




	def __init__(self):
		super (dumpBreak, self).__init__ ("dbreak", gdb.COMMAND_USER)
	 
	def invoke(self, arg, from_tty):
		args = arg.split(' ')
		self.location = gdb.Breakpoint(args[0]).location
		self.mem = args[1]
		gdb.events.stop.connect(self.stop_handler)

	 
dumpBreak()