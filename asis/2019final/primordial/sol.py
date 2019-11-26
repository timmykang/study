import gmpy2
import math
from Crypto.Util.number import *
from prob import primorial
#find a, b satisfy len(bin(p)[2:]) = 512
# a = primorial(379)
# b = primorial(29)
'''
a = (1 << 6)
b = (1 << 1)

low_e = 1 << 35
high_e = 1 << 36 - 1
while(math.log(a,2) < 9):
    a = gmpy2.next_prime(a)
    b = 1 << 1
    while(math.log(b,2) < 5):
        b = gmpy2.next_prime(b)
        tmp_a = primorial(a)
        tmp_b = primorial(b)
        for r in range(10**3, 3*10**3, 2):
            low_p = low_e * tmp_a // tmp_b - r
            high_p = high_e * tmp_a // tmp_b - r
            if len(bin(low_p)[2:]) <= 512 and len(bin(high_p)[2:]) >= 512:
                #print a,b
                #break
                print r
'''
                
a = primorial(379)
b = primorial(29)
print a
print b

