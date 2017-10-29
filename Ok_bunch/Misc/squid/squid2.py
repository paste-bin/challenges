#!/usr/bin/python

def bob():
	j = taco()
	j = taco()
	s = 'ROBOTWARRIOR'.join(''.join([sniff(ord(x),j) for x in 'HAPPYSQUIDSINTHETREESTAKINGALLTHEFOOD']).split(chr(taco())))
	return s

def sniff(smell, nose):
	return chr((smell + nose) % (2<<7))

def scratch(face, itch):
	return [chr(ord(cell) ^ ord(lump) ^ 0x41) for cell, lump in zip(face, itch)]

def nose(head):
	return len(head)

def crab(onion):
	return scratch(onion[::-1], bob())

def taco(x=[]):
	k = len(x)/2 + 1
	x += [1,[b*2 for b in x if not type(b) == type([])][0:k/2],[(c+b[0])*b[0] for b in x if type(b) == type([]) for c in b if not type(c) == type([])][::k],[d+c[0] for b in x if type(b) == type([]) for c in b if type(c) == type([]) for d in c if not type(d) == type([])][::-k],x]
	m = sum([b+1 for b in x if not type(b) == type([])] + [(c)-4 for b in x if type(b) == type([]) for c in b if not type(c) == type([])] + [d+1 for b in x if type(b) == type([]) for c in b if type(c) == type([]) for d in c if not type(d) == type([])])
	return m

tears = raw_input("potato? ")
onionz = crab(tears)
if ''.join(onionz) == "`gPzB|~s{JeiLje|r{Lulb}\k}b{UGKH":
	print 'you win! The flag is:',
	print tears
