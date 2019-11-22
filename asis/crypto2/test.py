import random
import math
import string
import hashlib
from pwn import *
from Crypto.Util.number import *
def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def findmd5(xx):
    while(1):
        x = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
        if hashlib.md5(x).hexdigest()[-6:] == xx:
    	    return x

def findsha512(xx):
    while(1):
        x = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
        if hashlib.sha512(x).hexdigest()[-6:] == xx:
    	    return x

def findsha256(xx):
    while(1):
        x = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
        if hashlib.sha256(x).hexdigest()[-6:] == xx:
    	    return x
def findsha1(xx):
    while(1):
        x = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
        if hashlib.sha1(x).hexdigest()[-6:] == xx:
    	    return x

def findsha224(xx):
    while(1):
        x = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
        if hashlib.sha224(x).hexdigest()[-6:] == xx:
    	    return x

def findsha384(xx):
    while(1):
        x = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
        if hashlib.sha384(x).hexdigest()[-6:] == xx:
    	    return x

r = remote("37.139.9.232",28399)
x=r.recvline()
print x
xx=x[-7:-1]
print xx
if 'md5' in x:
	r.send(findmd5(xx)+'\n')
elif 'sha256' in x:
	r.send(findsha256(xx)+'\n')
elif 'sha224' in x:
	r.send(findsha224(xx)+'\n')
elif 'sha1' in x:
	r.send(findsha1(xx)+'\n')
elif 'sha384' in x:
	r.send(findsha384(xx)+'\n')
elif 'sha512' in x:
	r.send(findsha512(xx)+'\n')

def enoracle(x):
	r.recvuntil('uit oracle!\n')
	r.send('E\n')
	r.recvline()
	r.send(str(x)+'\n')
	r.recvuntil('= ')
	x=r.recvuntil('\n')[:-1]
	return int(x)

def flagoracle():
	print r.recvuntil('uit oracle!\n')
	r.send('F\n')
	r.recvuntil('= ')
	x=r.recvuntil('\n')[:-1]
	return int(x)

def phioracle(x):
	r.recvuntil('uit oracle!\n')
	r.send('P\n')
	r.recvline()
	r.send(str(x)+'\n')
	r.recvuntil('= ')
	x=r.recvuntil('\n')[:-1]
	return int(x)
def gcd(a, b):
    while (b != 0):
        temp = a % b
        a = b
        b = temp
    return abs(a)
print 111
flag = flagoracle()
print flag
a2 = enoracle(2)
a3 = enoracle(3)
a4 = enoracle(4)
a5 = enoracle(5)
n2 = a2*a2-a4
n3 = a3*a3-enoracle(9)
n4 = a4*a4-enoracle(16)
n5 = a5*a5-enoracle(25)
n6 = a2*a3-enoracle(6)
n=gcd(n2,n3)
n=gcd(n,n4)
n=gcd(n,n5)
n=gcd(n,n6)
ans = phioracle(n)
ans = ans+1
ans1 = ans*ans - 4*n
ans2 = isqrt(ans1)
ans2 = int(ans2)
p = (ans2 + ans)/2
q = (ans - ans2)/2
phi = (p-1)*(q-1)
print p
print q
phintwo = 0
phin = (p-1)*(q-1)
while(phin %2 == 0):
	phintwo = phintwo +1 
	phin = phin /2

print phintwo
