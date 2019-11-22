from pwn import *
import gmpy2
gmpy2.get_context().precision=2000
r=remote('reality.ctfcompetition.com',1337)
r.recvuntil(': ')
encflag = (r.recvuntil('\n')[:-1])
r.recvuntil(': ')
x1 = gmpy2.mpfr(r.recvuntil(', ')[:-2])
y1 = gmpy2.mpfr(r.recvuntil('\n')[:-1])
r.recvuntil(': ')
x2 = gmpy2.mpfr(r.recvuntil(', ')[:-2])
y2 = gmpy2.mpfr(r.recvuntil('\n')[:-1])
r.recvuntil(': ')
x3 = gmpy2.mpfr(r.recvuntil(', ')[:-2])
y3 = gmpy2.mpfr(r.recvuntil('\n')[:-1])
r.close()
tmp0 = (y2-y1)/(x2-x1)
tmp1 = (y3-y2)/(x3-x2)
tmp2 = (tmp0-tmp1)/(x1-x3)
tmp3 = (x1+x2+x3)
tmp4 = (x1*x1+x2*x2+x3*x3+x1*x2+x1*x3+x2*x3)
print tmp3
print tmp4
print tmp2


