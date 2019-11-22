#!/usr/bin/env python
#-*- coding:utf-8 -*-

import random
from flag import flag

def encrypt(msg, perm):
	W = len(perm)
	while len(msg) % (2*W):
		msg += "."
	msg = msg[1:] + msg[:1]
	msg = msg[0::2] + msg[1::2]
	msg = msg[1:] + msg[:1]
	res = ""
	for j in xrange(0, len(msg), W):
		for k in xrange(W):
			res += msg[j:j+W][perm[k]]
	msg = res
	return msg

def decrypt(msg1,perm):
	W=len(perm)
	y=msg1
	half = len(y)/2
	res = ''
	x=''
	for j in xrange(0, len(y), W):
	    for k in xrange(W):
	        res += y[j:j+W][perm[k]]
	msg = res
	msg = msg[-1:]+msg[:-1]
	msg1 = msg[:half]
	msg2 = msg[half:]
	for i in range(half):
	    x=x+msg1[i]+msg2[i]
	x = x[-1:]+x[:-1]
	return x

def encord(msg, perm, l):
	for _ in xrange(l):
		msg = encrypt(msg, perm)
	return msg

#W, l = 7, random.randint(0, 1337)
W=7
j=0
perm = range(W)
x=encrypt('adsfqwe123',[0,1,2,3,4,5,6])
print x
print decrypt(x,[0,1,2,3,4,5,6])
while(1):
    if j % 100000 == 0:
        print j
    enc = flag
    perm=range(W)
    random.shuffle(perm)
    for i in range(1337):
        j=j+1
        enc = decrypt(enc,perm)
        if enc[:5] == 'ASIS{':
        	print enc

