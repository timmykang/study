#!/usr/bin/env python

import gmpy
from Crypto.Util.number import *
from flag import flag
import random
from operator import mul

def xirsa(msg, nbit, l):
    x, y = [getRandomInteger(nbit) for _ in '01']
    while True:
        Z = [random.randint(2, 19) for _ in xrange(l)]
        if len(set(Z)) >= l:
            break
    Z=[7,5,4,9,11]
    P = [gmpy.next_prime(x**Z[i] + y**Z[i]) for i in xrange(l)]
    print Z
    print x
    print y
    print P[0]*P[4]
    print P[1]*P[2]*P[3]
    #print P
    n, e = reduce(mul, P), 0x10001
    c = pow(bytes_to_long(msg), e, n)
    return Z, long(n), long(c) # Debug: remove Z in final version!

Z, n, c = xirsa(flag, 128, 5)
'''
print 'Z =', Z
print 'n =', n
print 'c =', c
'''
