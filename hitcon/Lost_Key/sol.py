from pwn import *
from gmpy import *
from Crypto.Util.number import *
r = remote('18.179.251.168',21700)
r.recvuntil('\n')
encflag = r.recvuntil('\n')[:-1]
def calA(x):
	if len(x)%2 == 1:
		x='0'+x
	r.recvuntil(': ')
	r.send('A\n')
	r.recvuntil(': ')
	r.send(x+'\n')
	return r.recvuntil('\n')[:-1]

def calB(x):
	if len(x)%2 == 1:
		x='0'+x
	r.recvuntil(': ')
	r.send('B\n')
	r.recvuntil(': ')
	r.send(x+'\n')
	return r.recvuntil('\n')[:-1]

def A(x):
	x=hex(x)[2:]
	i=calA(x)
	return int(i,16)

def B(x):
	x=hex(x)[2:]
	i=calB(x)
	return int(i,16)

encflag1= int(encflag,16)
x1 = A(3)
x2 = A(9)
n1=abs(x1*x1-x2)
for i in range(2):
	x=A(i+3)
	y=A((i+3)*(i+3))
	n1=GCD(n1,abs(x*x-y))


x1=pow(A(2),8,n1)
k1 = 0
y0 = B(encflag1)
i=1
print invert(n1,256)
for j in range(130):
	k=pow(x1,j+1,n1)
	y=B(k*encflag1)
	k1 = 256*k1 + ((256-y)*invert(n1,256))%256
	if pow(256,j+1) > n1:
		break
	i=i+1

flag= (n1*k1)/pow(256,i)
print hex(flag)[2:].decode('hex')
r.close()
#hitcon{1east_4ign1f1cant_BYTE_0racle_is_m0re_pow3rfu1!}
