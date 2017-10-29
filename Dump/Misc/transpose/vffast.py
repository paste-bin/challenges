#!/usr/bin/python

import os

import subprocess

words = []

with open('./common.txt', 'r') as dict_words:
	for word in dict_words:
		words.append(word.rstrip())

print 'hello' in words
	


def find_word(word, end_word=False):

	format_string = "^{0}".format(word)
	if end_word:
		format_string += '$'
	proc = subprocess.Popen(["egrep " + format_string + " /usr/share/dict/words"],
			stdout=subprocess.PIPE,
			shell=True)

	(out, err) = proc.communicate()
	return len(out.splitlines())

def valid(string, end_word=False):
	''' Get the most recent word
	(that is after the last space)
	and see if it has any hits in the word search'''

	last_space = string.rfind(' ')
		
	word = string[last_space + 1:]
	is_word = False
	if word in words:
		is_word = True
		print "String: {0}".format(string)
	if end_word == False:
		for w in words:
			if word in w:	
#				print "String: {0} Count: {1}".format(string, is_word)
				return True
	


#	print "String: {0} Count: {1}".format(string, is_word)
	return is_word
	


	

checked = []


def dp(built_string, left_overs):

	if len(left_overs) == 0:
		return [built_string]

	candidates = []
	for x in range(len(left_overs)):
		char = left_overs[x]
		word = built_string + char
		if word in checked:
#			print 'Already done ' + word
			continue
		else:
			checked.append(word)

		if char == ' ' and not valid(built_string, end_word=True):
			# if the previous thing isn't a word
			# then don't continue
			continue
		
		new_left_overs = [a for a in left_overs]
		del new_left_overs[x]
		if valid(built_string + char):
			candidates.extend(dp(word, new_left_overs))
	return candidates
		




string = raw_input("Enter string:")
left_overs = [b for b in string]
print dp('', left_overs)
		






