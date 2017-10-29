# md5 hashing
# Andrew Bennett
# 2016-03-29
# for Freelancer CTF
#
# idea: given the hash of a phone number, brute force it
# hints/framework: given a script to hash an MD5 number in python
#
# this code will crack the hash
#
# takes ~2 minutes on my VM to try all possible cases
#
# setup: use the given code to hash the phone number we want them to crack
# have a phone with that number that one of the execs is holding + can reply with the flag
#
# challenge text:
# <Jordan?> forgot his phone number again. Fortunately, he's stored a hash of it!
# md5: <insert hash here>


"""
give this to students
"""

import hashlib

m = hashlib.md5()
m.update("0411123456")
print m.hexdigest()


"""
hint #1:
    mystring = str(1234)
"""

"""
hint #2:
    myotherstring = "5" + str(1234) + "9"
"""

"""
hint #3:
    all the flags look like flag{....}
"""

"""
hint #4:
    maybe if you text Jordan he'll have the flag?
"""

"""
here's my solution
"""

startnum = 400000000
endnum   = 499999999

for i in xrange(startnum, endnum):
    to_hash = "0" + str(i)
    a = hashlib.md5()
    a.update(to_hash)
    if a.hexdigest() == m.hexdigest():
        print "yay!"
        print "0" + str(i) 

