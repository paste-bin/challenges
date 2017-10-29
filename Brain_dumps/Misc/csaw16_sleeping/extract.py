#!/usr/bin/python
import sys
lines = ""
with open("file") as f:
	lines += ''.join(f.readlines())

sys.stdout.write(lines[:20872])

