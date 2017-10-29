#!/usr/bin/env python

funcs_prog = """

#include <stdio.h>
#include <stdlib.h>
#define FLAG_LEN 46
#define DEBUG 0

"""
func_template = """
extern void func{num}(unsigned char *buf) {{
	unsigned char rand[FLAG_LEN] = {{{rand_list}}};
	unsigned int offset = buf[{num}]%FLAG_LEN;
	unsigned int index = 0;
	for (index = 0; index < FLAG_LEN; index++) {{
		buf[(unsigned int)((index + offset) % FLAG_LEN)] ^= rand[index];
	}}
	if (DEBUG) {{
		printf("||");
		for (index = 0; index < FLAG_LEN; index++) {{
			printf("%2hhx",buf[index]);
		}}
		printf("**\\n");
	}}

}}
"""
def gen_func(rand_list, x):
	def func(buf):
		# simulate the c program
		# print ''.join([hex(y)[2:] for y in buf])
		offset = buf[x]%FLAG_LEN
		index = 0
		while index < FLAG_LEN:
			buf[(index + offset) % FLAG_LEN] = (0x00FF & (buf[(index + offset) % FLAG_LEN])) ^ (0x00FF & rand_list[index])
			index += 1
	return func

buf = [ord(x) for x in list("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")]

# flag = [ord(x) for x in list("AAAAAAAAAAAAAAAhello this is the flagAAAABBBBB")]
flag = [ord(x) for x in list("COMP6445{bonus_points_for_hacking_the_linker!}")]
print len(buf)
FLAG_LEN = 46
import random
func_list = []

for x in range(FLAG_LEN-1):
	rand_list = [random.randint(0,0xff) for y in range(FLAG_LEN)]
	rlist = ', '.join([hex(y) for y in rand_list])
	funcs_prog += func_template.format(num=x, rand_list=rlist)
	func_list.append(gen_func(rand_list, x))

nums  = range(FLAG_LEN-1)
correct_order = []

while len(correct_order) != len(nums):
	rand_pos = random.randint(0,len(nums)-1)
	if rand_pos not in correct_order:
		correct_order.append(rand_pos)

print "The correct order is "
print correct_order

for func_index in correct_order:
	func_list[func_index](buf)

# func_list.append(gen_func(nr, FLAG_LEN-1))

offset = buf[(FLAG_LEN-1)]%FLAG_LEN
not_so_rand = [b^f for b,f in zip(buf, flag)]
nr = not_so_rand[offset:] + not_so_rand[:offset]
rlist = ', '.join([hex(y) for y in nr])
funcs_prog += func_template.format(num=FLAG_LEN-1, rand_list=rlist)

# simulate the c program
offset = buf[(FLAG_LEN-1)]%FLAG_LEN
index = 0
while index < FLAG_LEN:
	buf[(index + offset) % FLAG_LEN] = (0x00FF & (buf[(index + offset) % FLAG_LEN])) ^ (0x00FF & nr[index])
	index += 1
print ''.join([hex(y)[2:] for y in buf])


with open('funcs.c', 'w') as f:
	f.write(funcs_prog)



