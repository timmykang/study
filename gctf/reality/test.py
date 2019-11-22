from pwn import *
x=[]
coef1=[]
coef2=[]
coef3=[]
while(1):
	i=0
	r=remote('reality.ctfcompetition.com',1337)
	r.recvuntil(': ')
	y=(r.recvuntil('\n')[:-1])
	if y in x:
		i = 1
	x.append(y)
	r.recvuntil('\n')
	tmp0 = (r.recvuntil('\n')[:-1])
	tmp1 = (r.recvuntil('\n')[:-1])
	tmp2 = (r.recvuntil('\n')[:-1])
	coef1.append(tmp0)
	coef2.append(tmp1)
	coef3.append(tmp2)
	if i == 1:
		print y
		index1 = x.index(y)
		print tmp0
		print tmp1
		print tmp2
		print coef1[index]
		print coef2[index]
		print coef3[index]
		break
	r.close()


