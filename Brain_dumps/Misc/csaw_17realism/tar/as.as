BITS 32
global _start
_start:
mov eax, [0x1234]
cmp     eax, 0x67616C66
jnz    	fail        ; fail

l1:
movaps  xmm0, [0x1238]
movaps  xmm5, [0x7C00]
pshufd  xmm0, xmm0, 11110b
mov     si, 8
l2:
movaps  xmm2, xmm0
mov	eax, 0x7D90
add	eax, esi
andps   xmm2, [eax]

psadbw  xmm5, xmm2
movaps  [0x1268], xmm5
mov     di, 0x1268
shl     edi, 0x10
mov     di, 0x1270
mov     dx, si
dec     dx
add     dx, dx
add     dx, dx
cmp     edi, [edx+7DA8h]
jnz     fail

l3:
dec     si
test    si, si
jnz     l2

win:
mov     [0x1278], BYTE 0x0A
mov     bx, 0x1266
mov     di, 0x7D70       ; Win Flag
test    bx, bx
nop

fail:
jmp fail

bbbb:
	dq 0x0
	dq 0x0

_data:
section .attach
incbin "main.bin"
