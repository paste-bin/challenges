# Differently-sized files
# one has the flag, and that's the one that's a different size to the others
# 
# Idea: Emily Olorin
#
# Implementation: Andrew Bennett
# Freelancer CTF
# 2015-04-06

# generate a large number of files -- say 1000?
# make them all be full of random crap that's indistinguishable from the correct answer
# but one of them is a bigger size and has a clearly correct answer


# eg: if you can grep for "flag{" and find it, we've failed

# maybe we could have a thing saying "put flag{..} around the answer, you'll know when you find it"
# and have a bunch of random crap in each file, but one has actual words (but leet words so you can't tell it's obviously that)

# so: generate a bunch of "words" made of random noise, random assortments of {a-zA-Z0-9}, of len {randint(3,30)}
# and make one file have the same line over and over again which is the flag of some sort
# eg maybe "y0u-f0und-iT-w3ll-d0n3"
# have spaces or dashes around words otherwise




# ideal output:

#word-word-longword-word word-longerword word-word-word etc

NUM_FILES = 256
NUM_WORDS = 10000
CUTOFF_LEN = 65535


import random

lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"

allchars = lower*10 + upper*2 + numbers*1 + "\n"*3

def space():
    r = random.randint(0,5)
    if r <= 2:
        return " "
    else:
        return "-"


def wordlen():
    return int(random.gauss(7,7)+1)

def word(length):
    try:
        return ''.join(random.sample(allchars, length))
    except Exception, e:
        return "wow!"


outputs = []
for attempt in xrange(0,NUM_FILES):
    output = ""
    for thing in xrange(0,NUM_WORDS):
        output += str(word(wordlen())) + space()
    outputs.append(output)


for thing in xrange(0,len(outputs)):
    print len(outputs[thing]),
    with open("f"+str(thing), "w") as outf:
        outf.write(outputs[thing][:CUTOFF_LEN])



