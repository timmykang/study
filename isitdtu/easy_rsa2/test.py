from Crypto.Util.number import *
import gmpy2
p1 = getPrime(512)
p2 = gmpy2.next_prime(p1)
q1 = getPrime(512)
q2 = gmpy2.next_prime(q1)
n = p1*p2*q1*q2
e = 65537
phi = (p1-1)*(p2-1)*(q1-1)*(q2-1)
d = gmpy2.invert(e,phi)
data1 = pow(p1+q2,65537,n)
data2 = pow(p2+q1,65537,n)
print p2-p1
print q2-q1
print ((data1-data2)%n)%65537
