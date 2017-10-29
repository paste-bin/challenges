#!/usr/bin/python
import random

string = raw_input("Enter String:")

shuffleList = []


for x in string:
	pos = random.randint(0,len(shuffleList))
	shuffleList.insert(pos, x)
print ''.join(shuffleList)
