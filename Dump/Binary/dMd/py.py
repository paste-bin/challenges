#!/usr/bin/python

import hashlib


m = hashlib.md5('grape').hexdigest()

print m


m = hashlib.md5(m).hexdigest()

print m

