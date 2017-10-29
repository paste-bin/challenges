#!/usr/bin/python
import random

from random import randint



# grid = []

height = 50
grid = []

for x in range(height):
	grid.append([' '] * height)



for a in range(100):
	x = 0
	with open('./maps/' + str(a), 'r') as f:
		y = 0
		for line in f:
			line = line.rstrip()
			y = 0
			for c in line:
				if grid[x][y] == ' ':
					grid[x][y] = c
				y += 1
			x += 1

for x in range(height):
	for y in range(height):
		print grid[x][y],
	print 



