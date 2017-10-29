#!/usr/bin/env python
# -*- coding: utf-8 -*-

import emoji
import random
def eprint(thing):
    return emoji.emojize(thing, use_aliases=True)


MAX = 3
flagbin = "01011001011011110111010100100000011001000110100101100100001000000110100101110100001000010010000001010111011001010110110001101100001000000110010001101111011011100110010100101110001000000101010001101000011001010010000001100110011011000110000101100111001000000110100101110011001000000110011001101100011000010110011101111011011110010011000001110101010111110110001100110100011011100101111101100011001100000110010001100101010111110111011100110001011101000110100001011111011001010110110100110000011010100110100101111101"

flagtxt = "You did it! Well done. The flag is flag{y0u_c4n_c0de_w1th_em0ji}"

left =  [":arrow_left:", ":arrow_lower_left:", ":arrow_upper_left:"]
right = [":arrow_right:", ":arrow_lower_right:", ":arrow_upper_right:"]

extended_left  = [":leftwards_arrow_with_hook:", ":arrow_backward:", ":rewind:"]
extended_right = [":rightwards_arrow_with_hook:", ":arrow_forward:", ":fast_forward:"]

for thing in left:
    eprint(thing)
for thing in right:
    eprint(thing)

for thing in extended_left:
    eprint(thing)

for thing in extended_right:
    eprint(thing)

def randint():
    return random.randint(0, MAX-1)

def print_rand(one):
    extended = randint()

    if extended == 1:
        if one is False:
            return extended_left[randint()]
        else:
            return extended_right[randint()]
    else:
        if one is False:
            return left[randint()]
        else:
            return right[randint()]


flag_string = []

def print_flag():
    
    for bit in flagbin: 
        if bit == "1":
            flag_string.append(eprint(print_rand(True)))
        else:
            flag_string.append(eprint(print_rand(False)))

print_flag()

print ' '.join(flag_string)


