#!/usr/bin/env python

import os
import json
import base64

from team import encrypt, decrypt
from aes_common import *
msg = "GET REKT!!! points pls"
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
	cipher = chunks(base64.b64decode(string), BLOCK_SIZE)
	plain = team["decrypt"](cipher)
	return ''.join(plain)


def encryptMain(team):

	print "Enter your 'thought of the day'"
	tod = raw_input(">")
	data = {}
	data["name"] = "mr joe"
	data["tod"] = tod
	data["ZapCode"] = '1'
	cerial = json.dumps(data)
	print "Encrypting " + cerial
	print wrap_enc(cerial, team)
# Encrypting {"name": "mr joe", "tod": "asdflkhasdflkasdf", "ZapCode": "1"}
# /yen0KKfu4MXdhCXeFASgxJ4RUDco15cOoco1gG4VwiULVCLIVEnH6plgWNUxX##___7alIq956eLOR547uyuA==
# /yen0KKfu4MXdhCXeFASgxJ4RUDco15cOoco1gG4VwiULVCLIVEnH6plgWNUxX1VZapCodeq956eLOR547uyuA==
# /yen0KKfu4MXdhCXeFASgxJ4RUDco15cOoco1gG4VwiULVCLIVEnH6plgWNUxX1VD7k7alIq956eLOR547uyuA==
# /yen0KKfu4MXdhCXeFASgxJ4RUDco15cOoco1gG4VwiULVCLIVEnH6plgWNUxX1VD7k7alIq956eLOR547uyuA==
# /yen0KKfu4MXdhCXeFASgxJ4RUDco15cOoco1gG4VwiULVCLIVEnH6plgWNUxX1VD7k7alIq956eLOR547uyuA==
# Encrypting {"name": "mr joe", "tod": "asdflkhasdflkasdf1111", "ZapCode": "1"}
# /yen0KKfu4MXdhCXeFASgxJ4RUDco15cOoco1gG4VwhSjHy17QR3qf3c3XUh2rH/S5cfOUdaFRieKXbqCt7NzI2pCKYxLDgs9tlP71dKVLE=
# /yen0KKfu4MXdhCXeFASgxJ4RUDco15cOoco1gG4VwhSjHy17QR3qf3c3XUh2rH/S*cfOUd*FRieKXbqC*7NzI2pCKYxLDgs9tlP71dKVLE=
# /yen0KKfu4MXdhCXeFASgxJ4RUDco15cOoco1gG4VwhSjHy17QR3qf3c3aUh2rH/S5cfOUdaFRieKXbqCt7NzI2pCKYxLDgs9tlP71dKVLE=
# /yen0KKfu4MXdhCXeFASgxJ4RUDco15cOoco1gG4VwhSjHy17QR3qfAc3XUh2rH/S5cfOUdaFRieKXbqCt7NzI2pCKYxLDgs9tlP71dKVLE=

def decryptMain(team):
	"""
		Attempt a decryption and check if their attack worked
	"""
	print "Enter a string to decrypt"
	string = raw_input(">")
	plain = wrap_dec(string, team)
	print plain

	counter = ord(plain[-1])
	if counter < 0 or counter > 16:
		print "Incorrect Padding!"

	for p in plain[-counter:]:
		if ord(p) != counter:
			print "Incorrect Padding!"
			return
	plain = plain[:-counter]

	
	print "Correct Padding!"
	if plain == msg:
		print "successfully encrypted " + msg
		# give team flag
		return
	try: 
		data = json.loads(plain)
		if "admin" in data:
			if data["admin"] == 1:
				print "successfully Authenticated as admin!"
			else:
				print "did not authenticate!"
		else:
			print "admin parameter missing from decryption"
	except:
		print "invalid json"

	return


teams = []
teams.append(
	{
		"name" : "team0",
		"code" : "banana",
		"encrypt" : encrypt,
		"decrypt" : decrypt
	}
)

teams.append(
	{
		"name" : "team1",
		"code" : "banana",
		"encrypt" : encrypt,
		"decrypt" : decrypt
	}
)

for team in teams:
	team["cipher"] = wrap_enc(team["code"], team)
	if pad("banana") not in ''.join(team["decrypt"](team["encrypt"](chunks(pad("banana"),BLOCK_SIZE)))):
		print "BROKEN TEAM: " + team["name"]
		teams.remove(team) 

def welcome():
	print "Welcome Hackers, to crypto warz!!"


def get_target():
	print "Select a team to target:"
	i = 0
	for team in teams:
		print str(i) + ") " + team["name"]
		i += 1
	return get_num_in_range(0, 1)

def get_num_in_range(low, high):	
	try:
		choice = int(raw_input(">"))
		if choice < low or choice > high:
			valid = False
	except:
		valid = False

	if not valid:
		print "invalid selection"
		return get_target()
	return choice

# print deets 
def print_team_details(attack_choice):
	print "You have selected: " + teams[attack_choice]["name"]
	print "Decode their cipher: " + teams[attack_choice]["cipher"] + " for 100 points"
	print "Encode the string '" + msg + "' to get 100 points"
	print "Flip the encrypted 'admin' parameter in thought of the day token to get 100 points"

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
	choice = get_num_in_range(0, 1)



welcome()
attack_choice = get_target()
print_team_details(attack_choiceattack_choice)
choice = get_option()

if choice == "0":
	encryptMain(teams[attack_choice])
elif choice == "1":
	decryptMain(teams[attack_choice])



