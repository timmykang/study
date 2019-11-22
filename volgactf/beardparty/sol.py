from pwn import *
from sboxes_mod import S
import encrypted
cipher = encrypted.x
Sinv=[[],[],[],[]]

for i in range(1024):
	Sinv[0].append(S[0].index(i))
	Sinv[1].append(S[1].index(i))
	Sinv[2].append(S[2].index(i))
	Sinv[3].append(S[3].index(i))


def Give(r,x):
	r.recvline()
	x=x.encode('base64')
	r.send(x)
	kk=r.recvline()[:-1].decode('base64').encode('hex')
	r.recvline()
	return kk

cipher = cipher.decode('base64').encode('hex')
r=remote('beard-party.q.2019.volgactf.ru', 7777)
print cipher
print Give(r,'a*9')
print Give(r,'a*8+b')

