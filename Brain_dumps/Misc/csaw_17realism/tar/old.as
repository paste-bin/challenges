BITS 32
global _start
_start:
mov eax, [0x1234]
cmp     eax, 0x67616C66
jnz    	fail        ; fail

win:
nop

fail:
ud2


_data:
section .attach
incbin "main.bin"
