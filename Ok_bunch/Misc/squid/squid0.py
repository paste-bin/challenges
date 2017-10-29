#!/usr/bin/python

def bob():
	j = taco()
	j = taco()
	s = 'kbob.join("([]".split_sniff())'.join(''.join([sniff(ord(x),j) for x in 'SUPERBOBSAVESEVERYONE']).split(chr(taco())))
	return s

def sniff(smell, nose):

	return chr((smell + nose) % (2<<7))

def nose(head):
	return len(head)

def crab(onion):
	prawn = nose(bob())
	return [sniff(ord(layer), prawn) for layer in onion[::-2]]

def taco(x=[]):
	k = len(x)/2 + 1
	x += [1]
	m = sum([b+1 for b in x if not type(b) == type([])] + [(c)-4 for b in x if type(b) == type([]) for c in b if not type(c) == type([])] + [d+1 for b in x if type(b) == type([]) for c in b if type(c) == type([]) for d in c if not type(d) == type([])])

	return m

tears = raw_input("carrots? ")

onionz = crab(tears)

password = ['c', 'd', 'c', 'c', 'V', 'X', 't', 'c', 'Z', 'i', 'i', '^', '`', 't', '[', 'i', 'X', '[']
for nail, gear in zip(password, onionz):
	if not nail == gear:
		print 'you loose'
		break
else:
	print 'you win! The flag is:',
	print tears[1::2]

