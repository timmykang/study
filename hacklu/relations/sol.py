#!/usr/bin/env python
from pwn import *
from base64 import *
from Crypto import *

def run(what, mes):
	r.recvuntil('*\n')
	r.send(what+'\n')
	r.recvuntil('>>> ')
	r.send(mes+'\n')
	r.recvuntil('is  ')
	return r.recv(90)

def xor(mes):
	return b64decode(run('XOR',mes))

def add(mes):
	return b64decode(run('ADD',mes))

def dec(mes):
	r.recvuntil('*\n')
	r.send('DEC\n')
	r.recvuntil('>>> ')
	r.send(mes+'\n')
	r.recvuntil('is  ')
	return r.recv(65)



b=1
key=0
key2=1
r=remote('arcade.fluxfingers.net',1821)

for i in range(0,128):
	print i
	d=hex(b)[2:]
	if add(d) == xor(d):
		print 1
	else:
		key = key +key2
		print 2
	key2= key2*2
	b=b*2

z=str(-key)
y=str(key)
if add(z) == xor(y):
	print 1
key = hex(key)
if len(key) % 2 == 0:
	key1 = key[2:].decode('hex')
	print 1
else:
	key1 = ('0'+key[2:]).decode('hex')

a= len(key1)
print a
key1 = '\x00'*(16- len(key1)) + key1 
key2 = b64encode(key1)
print dec(key2)
print dec(key1)


r.close()

