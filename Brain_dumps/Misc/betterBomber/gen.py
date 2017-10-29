#!/usr/bin/python
import random

from random import randint



grid = []

height = 50
flag = []

col = 3

f = [(24,col),(25,col),(26,col),(27,col),(28,col),(29,col)]
col += 1
f += [(24,col)      ,(26,col),					]
col += 1
f += [(24,col)      ,(26,col),					]

col += 1
col += 1

r = [		(25,col),(26,col),(27,col),(28,col),(29,col)]
col += 1
r += [		(25,col)     					]
col += 1
r += [		(25,col)      					]

col += 1
col += 1



o1 = [		(25,col),(26,col),(27,col),(28,col),(29,col)]
col += 1
o1 += [		(25,col),     						(29,col)]
col += 1
o1 += [		(25,col),     						(29,col)]
col += 1
o1 += [		(25,col),(26,col),(27,col),(28,col),(29,col)]

col += 1
col += 1


o2 = [		(25,col),(26,col),(27,col),(28,col),(29,col)]
col += 1
o2 += [		(25,col),     						(29,col)]
col += 1
o2 += [		(25,col),     						(29,col)]
col += 1
o2 += [		(25,col),(26,col),(27,col),(28,col),(29,col)]

col += 1


col += 1
t = [(24,col)      				]
col += 1
t += [(24,col)      				]
col += 1
t += [(24,col),(25,col),(26,col),(27,col),(28,col),(29,col)]
col += 1
t += [(24,col)   			]
col += 1
t += [(24,col)      				]

col += 1
col += 1

l = [(24,col),(25,col),(26,col),(27,col),(28,col),(29,col)]
col += 1
l += [												(29,col)      	]
col += 1
l += [												(29,col)     ]

col += 1
col += 1



o3 = [		(25,col),(26,col),(27,col),(28,col),(29,col)]
col += 1
o3 += [		(25,col),     						(29,col)]
col += 1
o3 += [		(25,col),     						(29,col)]
col += 1
o3 += [		(25,col),(26,col),(27,col),(28,col),(29,col)]

col += 1
col += 1


o4 = [		(25,col),(26,col),(27,col),(28,col),(29,col)]
col += 1
o4 += [		(25,col),     						(29,col)]
col += 1
o4 += [		(25,col),     						(29,col)]
col += 1
o4 += [		(25,col),(26,col),(27,col),(28,col),(29,col)]

col += 1
col += 1


p = [(24,col),(25,col),(26,col),(27,col),(28,col),(29,col)]
col += 1
p += [(24,col)      ,(26,col),					]
col += 1
p += [(24,col),(25,col),(26,col),					]

col += 1
col += 1

s = [		(25,col),(26,col),(27,col),			(29,col)]
col += 1
s += [		(25,col),     	  (27,col),			(29,col)]
col += 1
s += [		(25,col),     	  (27,col),			(29,col)]
col += 1
s += [		(25,col),		  (27,col),(28,col),(29,col)]

col += 1
col += 1

flag = f + r + o1 + o2 + t + l +o3 +o4 + p + s


# for x in range(height):
# 	grid.append([])
# 	for y in range(height):
# 		# grid[x].append(str(x) + ":" + str(y))
# 		grid[x].append('#')


for a in range(100):
	with open('./maps/'+str(a), 'w') as f:
		for x in range(height):
			for y in range(height):
				if (x,y) in flag:
					f.write(' ')
				else:
					if randint(0,6) == 0:
						f.write('#')
					else:
						f.write(' ')

			f.write('\n')
	

