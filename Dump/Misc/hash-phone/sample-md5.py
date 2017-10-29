import hashlib

m = hashlib.md5()
m.update("0400000000")
print m.hexdigest()

