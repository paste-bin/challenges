#!/usr/bin/env python

import os
import sys
import json
import base64

from team import team
from aes_common import *
msg = "GET REKT!!!! points pls"

encFlag = ""
adminFlag = ""
crackFlag = ""

with open("encFlag.txt", 'r') as f:
	encFlag = f.readlines()[0].rstrip()

with open("adminFlag.txt", 'r') as f:
	adminFlag = f.readlines()[0].rstrip()

with open("crackFlag.txt", 'r') as f:
	crackFlag = f.readlines()[0].rstrip()



def wrap_enc(string, team):
	"""
		Use the team supplied encrytion function
		and then base64 encode it.
	"""
	blocks = chunks(pad(string), BLOCK_SIZE)
	return base64.b64encode(''.join(team["encrypt"](blocks)))

def wrap_dec(string, team):
	"""
		Use the team supplied decrytion function
		and then base64 encode it.
	"""
	try:
		cipher = chunks(base64.b64decode(string), BLOCK_SIZE)
		plain = team["decrypt"](cipher)
	except:
		print "Bad decryption"
		return None
	return ''.join(plain)


def encryptMain(team):

	print "Enter your 'thought of the day'"
	tod = raw_input(">")
	cerial = '{{"name":"mr joe","tod":"{tod}","admin":0}}'.format(tod=tod)
	print "Encrypting " + cerial
	print wrap_enc(cerial, team)
	sys.stdout.flush()

def decryptMain(team):
	"""
		Attempt a decryption and check if their attack worked
	"""
	print "Enter a string to decrypt"
	string = raw_input(">")
	plain = wrap_dec(string, team)
	if plain == None:
		return
	# print plain
	sys.stdout.flush()

	counter = ord(plain[-1])
	if counter < 0 or counter > 16:
		print "Incorrect Padding!"

	for p in plain[-counter:]:
		if ord(p) != counter:
			print "Incorrect Padding!"
			return
	plain = plain[:-counter]
	sys.stdout.flush()

	
	print "Correct Padding!"
	if plain == msg:
		print "successfully encrypted " + msg
		# give team flag
		print "Have a flag: " + encFlag
		sys.stdout.flush()
		return
	try: 
		data = json.loads(plain)
		if "admin" in data:
			if data["admin"] == 1:
				print "successfully Authenticated as admin!"
				print "Have a flag: " + adminFlag
				sys.stdout.flush()
			else:
				print "did not authenticate!"
				sys.stdout.flush()
		else:
			print "admin parameter missing from decryption"
			sys.stdout.flush()
	except:
		print "invalid json"
		sys.stdout.flush()
	return


team["cipher"] = wrap_enc(team["code"], team)

if pad("banana") not in ''.join(team["decrypt"](team["encrypt"](chunks(pad("banana"),BLOCK_SIZE)))):
	print "BROKEN TEAM: " + team["name"]
	sys.stdout.flush()
	teams.remove(team) 

def welcome():
	print "Welcome Hackers, to crypto warz!!"
	sys.stdout.flush()

def get_num_in_range(low, high):	
	valid = True
	choice = -1
	try:
		choice = int(raw_input(">"))
		if choice < low or choice > high:
			valid = False
	except:
		valid = False

	if not valid:
		print "invalid selection"
		sys.stdout.flush()
		return get_num_in_range(low, high)
	return choice


# print deets 
def print_team_details():
	print "You are attacking: " + team["name"]
	print "Decode their cipher: " + team["cipher"] + " for 100 points"
	print "Encode the string '" + msg + "' to get 100 points"
	print "Flip the encrypted 'admin' parameter in thought of the day token to get 100 points"
	sys.stdout.flush()

def get_option():
	"""
		ask for choice of 
		I've decoded their cipher
		or
		I want to encrypt a thing
		or
		I want to attempt a decrypt
	"""
	print "What do you want to do?"
	print "0) Encrypt 'thought of the day' token"
	print "1) Attempt Decrypt"
	print "2) Submit cracked cipher"
	sys.stdout.flush()
	choice = get_num_in_range(0, 2)
	return choice

def validateCrack(team):
	d = raw_input('>')
	if d == team["code"]:
		print "Have a flag: " + crackFlag
		sys.stdout.flush()
	else:
		print "nope"
		sys.stdout.flush()


welcome()
print_team_details()
choice = get_option()


if choice == 0:
	encryptMain(team)
elif choice == 1:
	decryptMain(team)
elif choice == 2:
	validateCrack(team)

# print wrap_enc(msg, team)


