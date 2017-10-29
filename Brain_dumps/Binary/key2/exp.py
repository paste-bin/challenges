import gdb
def hack(cur='', max=1):

	for c in range(ord('a'), ord('z')+1):

		gdb.execute("r <<< " + cur + chr(c), to_string=True)
		count = 0
		while True:
			try:
				gdb.execute('c', to_string=True)
			except:
				break
			count += 1
		print cur + chr(c) + " Gives :" + str(count)
		if count > max:
			print "FOUND " + chr(c)
			hack(cur + chr(c), max + 1)
			exit()
		


