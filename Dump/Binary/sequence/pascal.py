#!/usr/bin/python
import hashlib
import math

def nCr(n,r):
  f = math.factorial
  return f(n) / f(r) / f(n-r)
ans = ""
for a in range(20):
  for b in range(a+1):
    ans += str(nCr(a,b))
print hashlib.sha1(ans).hexdigest()
