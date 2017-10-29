#!/usr/bin/python


randomNum = 0 #0x47003e2b60022de2
nums = {}
# while True:
randomNum += 0x100000000
randomNum = 0
a = randomNum 
# a = c = 0x159ea7ba623eb94d
c = randomNum
d = 0x8000000000018001
c = a
# d:a = d * a
# 0xacf53dd311f7d1491363b187832394d
# d = 0xacf53dd311f7d14

# lots of magic later...
d = ( a + (((((a>>10)*0x18001))>>(15*4 - 10))>>3))>>1 


# so we've saved the overflow (which is small(ish(er))) into rdx at this point

a = a - d
# a = 0xacf53dd311f3c39

# right shift a right 1  0x1000000000000
# i.e lop off the last bit
# a = 0x567a9ee988f9e1c
a >>=1

a += d
# a = 0x1036fdcbc9af1b30)
# right shift a 46 to the right

a >>=46
# a = 0x40db
# lolz, leaves us with like 15 bits

d = 0x555555555555


a = a * d #(imul)
# a = 0x159e555555553fb7)

c = c - a 
# c = 0x52650ce97996
a = c
# a = 0x52650ce97996
# d = 0x1000 # page size 
# neg d 

# d = 0xfffff000
# signed extend mov d -> d
d = 0xfffffffffffff000

a = a & d
print hex(a)
# print hex(randomNum)
if a in nums:
	print 'found a collision'
	print hex(a)
	print "generated from "
	nums[a].append(hex(randomNum))
	print nums[a]
else:
	nums[a] = [hex(randomNum)]
# print hex(a)
# print hex(a)
# print  
# a = 0x52650ce97000

# Collisions:
#  0x656200000000
# 0x1656200000000
# 0x2656200000000
# 0x3656200000000
# 656200000
