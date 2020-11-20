from pwn import *
import os
import time

from Cryptodome.Cipher import AES
from Cryptodome.Util.number import *

from fertilizers import Fertilizer1, Fertilizer2, Fertilizer3
from utils import Drawer, banner1, banner2, banner3, flag
from sage.all import *

TARGET_LAYER = 9000
TARGET_BLOCKS = 16
BLOCK_SIZE = 16

r = remote('happy-farm.balsnctf.com', 4001)
#r = process('./chal1.py')

def coppersmith_howgrave_univariate(pol, modulus, beta, mm, tt, XX):

    dd = pol.degree()
    nn = dd * mm + tt

    if not 0 < beta <= 1:
        raise ValueError("beta should belongs in (0, 1]")

    if not pol.is_monic():
        raise ArithmeticError("Polynomial must be monic.")


    cond1 = RR(XX**(nn-1))
    cond2 = pow(modulus, beta*mm)

    cond2 = RR(modulus**(((2*beta*mm)/(nn-1)) - ((dd*mm*(mm+1))/(nn*(nn-1)))) / 2)

    detL = RR(modulus**(dd * mm * (mm + 1) / 2) * XX**(nn * (nn - 1) / 2))

    cond1 = RR(2**((nn - 1)/4) * detL**(1/nn))
    cond2 = RR(modulus**(beta*mm) / sqrt(nn))
    
    polZ = pol.change_ring(ZZ)
    x = polZ.parent().gen()

    gg = []
    for ii in range(mm):
        for jj in range(dd):
            gg.append((x * XX)**jj * modulus**(mm - ii) * polZ(x * XX)**ii)
    for ii in range(tt):
        gg.append((x * XX)**ii * polZ(x * XX)**mm)
    
    BB = Matrix(ZZ, nn)

    for ii in range(nn):
        for jj in range(ii+1):
            BB[ii, jj] = gg[ii][jj]

    BB = BB.LLL()

    new_pol = 0
    for ii in range(nn):
        new_pol += x**ii * BB[0, ii] / XX**ii

    potential_roots = new_pol.roots()

    roots = []
    for root in potential_roots:
        if root[0].is_integer():
            result = polZ(ZZ(root[0]))
            if gcd(modulus, result) >= modulus**beta:
                roots.append(ZZ(root[0]))
    return roots

def get_n(x):
    prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
    while(x.nbits() != 1024):
        for i in prime:
            if x % i == 0:
                x = x // i
    return x

def get_value(r):
    value = ''
    for i in range(22):
        tmp=r.recvline().split()
        for j in tmp:
            tmp_j = j.decode()
            if 'x' in tmp_j:
                value += tmp_j[:tmp_j.index('x')]
            else:
                value += tmp_j
    return bytes.fromhex(value)

def get_value1(r):
    value = ''
    for i in range(16):
        tmp=r.recvline().split()
        for j in tmp:
            tmp_j = j.decode()
            value += tmp_j
    value += '0'
    tmp=r.recvline().split()
    for j in tmp:
        tmp_j = j.decode()
        value += tmp_j
    return int(value,16)

def level1(r):
    r.recvuntil('seed:\n')
    seed = get_value(r)
    r.recvuntil('start date: ')
    start_date = bytes.fromhex(r.recvline()[:-1].decode())

    my_start_date0 = seed[:16].hex()
    my_seed0 = (start_date + seed[16:]).hex() 
    r.recvuntil('start date: ')
    r.sendline(my_start_date0)
    r.recvuntil('seed: ')
    r.sendline(my_seed0)
    r.recvuntil('layer: ')
    r.sendline('1')

    (r.recvline())

    cipher0 = get_value(r)
    r.recvuntil('start date: ')
    r.sendline(cipher0[-16:].hex())
    r.recvuntil('seed: ')
    r.sendline(cipher0.hex())
    r.recvuntil('layer: ')
    r.sendline('8999')
    
    r.recvline()

    onion = get_value(r)
    r.recvuntil('like? ')
    r.sendline(onion.hex())
    print('level 1 complete')

def level2(r):
    r.recvuntil('seed is\n')
    seed = bytes_to_long(get_value(r))
    n0 = (1<<3069) - seed
    r.recvuntil('layer: ')
    r.sendline('8999')
    r.recvline()
    r.recvuntil('onion\n')
    onion0 = bytes_to_long(get_value(r))
    
    n1 = (pow(onion0,pow(3,8998), n0) - (1<<1023)) % n0
    n = GCD(n1,n0)
    n = get_n(n)
    onion0 = onion0 % n

    r.recvuntil('seed: ')
    r.sendline(long_to_bytes(1<<1023).hex())
    r.recvuntil('layer: ')
    r.sendline('8999')

    r.recvuntil('you go\n')
    onion1 = get_value1(r)
    
    P = PolynomialRing(Zmod(n), 'x') #, implementation='NTL')
    x = P.gen()
    dd = 3

    # Tweak those
    beta = 1                                # b = N
    epsilon = beta / 20                      # <= beta / 7
    mm = ceil(beta**2 / (dd * epsilon))     # optimized value
    tt = floor(dd * mm * ((1/beta) - 1))    # optimized value
    XX = ceil(n**((beta**2/dd) - epsilon))  # optimized value

    for i in range(16):
        print('try ', i)
        tmp_onion1 = onion1 + (1<<32) * i
        tmp = onion1.bit_length() % 4
        if tmp == 0:
            tmp = 4
        tmp_onion1 = tmp_onion1 << (1020 - tmp_onion1.bit_length() + tmp)
        pol = (tmp_onion1 + x)**3 - onion0
        roots = (coppersmith_howgrave_univariate(pol, n, beta, mm, tt, XX))
        if len(roots) == 1:
            break
    real_onion1 = tmp_onion1 + roots[0]
    r.recvuntil('like? ')
    r.sendline(long_to_bytes(real_onion1).hex())
    print('level 2 complete')

def level3(r):
    r.recvuntil('layer: ')
    r.sendline('0')
    r.recvline()
    onion_0 = get_value(r)
    r.recvuntil('layer: ')
    r.sendline('1')
    r.recvline()
    onion_1 = get_value(r)
    r.recvuntil('layer: ')
    r.sendline('192')
    r.recvline()
    onion_192 = get_value(r)
    print(onion_0 == onion_192)
    r.recvuntil('layer: ')
    target_layer = pow(9000,3,192)
    r.sendline(str(target_layer))
    r.recvline()
    target_onion = get_value(r)

    r.recvuntil('like? ')
    r.sendline(target_onion.hex())
    print('level 3 complete')
    r.interactive()


level1(r)
level2(r)
level3(r)

#BALSN{It_is_W3!rd_Why_c4n_You_P1a4t_Onions_F4om_Seeds_OF_SUNFLOWER?}