#!/usr/bin/python

# this is a starting place for exploiting the 1337 Microprocessor
# it has some helpful functions
# use like this:
# (./helper.py ; cat ) | ./Q1Compiled


import subprocess
from struct import pack

# Wrappers 
quit = chr(0)
inc_reg_1 = chr(1)
dec_reg_1 = chr(2)
inc_reg_2 = chr(3)
dec_reg_2 = chr(4)
set_f = chr(5)
set_word = chr(6)
get = chr(7)
get_word = chr(8)
load_r1 = lambda r1: chr(9) + chr(r1)
load_r1_word = lambda r1: chr(10) + pack('<I', r1)
load_r1_word_signed = lambda r1: chr(10) + pack('<i', r1)
print_f = chr(11)
swap = chr(12)
je = lambda addr: chr(13) + chr(addr)
jz = lambda addr: chr(14) + chr(addr)
jmp = lambda addr: chr(15) + chr(addr)
admin_stats = chr(16)

# Helpers
load_r2 = lambda r2: swap + load_r1(r2) + swap
load_r2_word = lambda r2: swap + load_r1_word(r2) + swap
save_r1 = lambda addr: swap + load_r1(addr) + set + swap # lose r2
save_r1_word = lambda addr: swap + load_r1_word(addr) + set_word + swap # lose r2
save_r1_word_signed = lambda addr: swap + load_r1_word_signed(addr) + set_word + swap # lose r2

tape = []


# Extract the address of the 'tape' variable from the binary
odump = subprocess.check_output("objdump -x ./Q1Compiled | grep tape", shell=True)
tape_addr = int("0x" + odump[:odump.index(' ')], 16)


tape += load_r1(40) + print_f

while len(tape) < 40:
	tape += chr(0)

print ''.join(tape) + "Welcome to the 1337Micro!!!!"





