#!/usr/bin/python

import os

import subprocess


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
	count = find_word(string[last_space + 1:], end_word)
	print "String: {0} Count: {1}".format(string, count)
	return count > 0
	


	




def dp(built_string, left_overs):
	if len(left_overs) == 0:
		return built_string

	candidates = []
	for x in range(len(left_overs)):
		char = left_overs[x]
		if char == ' ' and not valid(built_string, end_word=True):
			# if the previous thing isn't a word
			# then don't continue
			continue
		
		new_left_overs = [a for a in left_overs]
		del new_left_overs[x]
		if valid(built_string + char):
			candidates.append(dp(built_string + char, new_left_overs))
	return candidates
		




string = raw_input("Enter string:")
left_overs = [b for b in string]

print dp('', left_overs)


		






