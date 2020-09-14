from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from os import urandom
import time

debug = True

# display matrix picture with 0 and X
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += '0' if BB[ii,jj] == 0 else 'X'
            a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        #print(a)

def coppersmith_howgrave_univariate(pol, modulus, beta, mm, tt, XX):
    """
    Coppersmith revisited by Howgrave-Graham
    
    finds a solution if:
    * b|modulus, b >= modulus^beta , 0 < beta <= 1
    * |x| < XX
    """
    #
    # init
    #
    dd = pol.degree()
    nn = dd * mm + tt

    #
    # checks
    #
    if not 0 < beta <= 1:
        raise ValueError("beta should belongs in (0, 1]")

    if not pol.is_monic():
        raise ArithmeticError("Polynomial must be monic.")

    #
    # calculate bounds and display them
    #
    """
    * we want to find g(x) such that ||g(xX)|| <= b^m / sqrt(n)
    * we know LLL will give us a short vector v such that:
    ||v|| <= 2^((n - 1)/4) * det(L)^(1/n)
    * we will use that vector as a coefficient vector for our g(x)
    
    * so we want to satisfy:
    2^((n - 1)/4) * det(L)^(1/n) < N^(beta*m) / sqrt(n)
    
    so we can obtain ||v|| < N^(beta*m) / sqrt(n) <= b^m / sqrt(n)
    (it's important to use N because we might not know b)
    """
    if debug:
        # t optimized?
        #print("\n# Optimized t?\n")
        #print("we want X^(n-1) < N^(beta*m) so that each vector is helpful")
        cond1 = RR(XX^(nn-1))
        #print("* X^(n-1) = ", cond1)
        cond2 = pow(modulus, beta*mm)
        #print("* N^(beta*m) = ", cond2)
        #print("* X^(n-1) < N^(beta*m) \n-> GOOD" if cond1 < cond2 else "* X^(n-1) >= N^(beta*m) \n-> NOT GOOD")
        
        # bound for X
        #print("\n# X bound respected?\n")
        #print("we want X <= N^(((2*beta*m)/(n-1)) - ((delta*m*(m+1))/(n*(n-1)))) / 2 = M")
        #print("* X =", XX)
        cond2 = RR(modulus^(((2*beta*mm)/(nn-1)) - ((dd*mm*(mm+1))/(nn*(nn-1)))) / 2)
        #print("* M =", cond2)
        #print("* X <= M \n-> GOOD" if XX <= cond2 else "* X > M \n-> NOT GOOD")

        # solution possible?
        #print("\n# Solutions possible?\n")
        detL = RR(modulus^(dd * mm * (mm + 1) / 2) * XX^(nn * (nn - 1) / 2))
        #print("we can find a solution if 2^((n - 1)/4) * det(L)^(1/n) < N^(beta*m) / sqrt(n)")
        cond1 = RR(2^((nn - 1)/4) * detL^(1/nn))
        #print("* 2^((n - 1)/4) * det(L)^(1/n) = ", cond1)
        cond2 = RR(modulus^(beta*mm) / sqrt(nn))
        #print("* N^(beta*m) / sqrt(n) = ", cond2)
        #print("* 2^((n - 1)/4) * det(L)^(1/n) < N^(beta*m) / sqrt(n) \n-> SOLUTION WILL BE FOUND" if cond1 < cond2 else "* 2^((n - 1)/4) * det(L)^(1/n) >= N^(beta*m) / sqroot(n) \n-> NO SOLUTIONS MIGHT BE FOUND (but we never know)")

        # warning about X
        #print("\n# Note that no solutions will be found _for sure_ if you don't respect:\n* |root| < X \n* b >= modulus^beta\n")
    
    #
    # Coppersmith revisited algo for univariate
    #

    # change ring of pol and x
    polZ = pol.change_ring(ZZ)
    x = polZ.parent().gen()

    # compute polynomials
    gg = []
    for ii in range(mm):
        for jj in range(dd):
            gg.append((x * XX)**jj * modulus**(mm - ii) * polZ(x * XX)**ii)
    for ii in range(tt):
        gg.append((x * XX)**ii * polZ(x * XX)**mm)
    
    # construct lattice B
    BB = Matrix(ZZ, nn)

    for ii in range(nn):
        for jj in range(ii+1):
            BB[ii, jj] = gg[ii][jj]

    # display basis matrix
    if debug:
        matrix_overview(BB, modulus^mm)

    # LLL
    BB = BB.LLL()

    # transform shortest vector in polynomial    
    new_pol = 0
    for ii in range(nn):
        new_pol += x**ii * BB[0, ii] / XX**ii

    # factor polynomial
    potential_roots = new_pol.roots()
    print("potential roots:", potential_roots)

    # test roots
    roots = []
    for root in potential_roots:
        if root[0].is_integer():
            result = polZ(ZZ(root[0]))
            if gcd(modulus, result) >= modulus^beta:
                roots.append(ZZ(root[0]))

    # 
    return roots

n = 0x914e0f4b603ac9ab6eb0796271fff8f6033aa612e04d95547109d025748e1c68672fe40459e71937e6a3f9156fd4713ad95a3198b318378565f53e46c6059e0f6ec973c09a4f588e8f9078e03af8a7ea6211169638efd7c5d5db179c37cdf4732aa5462bca7deab6c3c9c6b02a0491d8363495b1c834e7733eeccfa0aaa6d021
cf = 0x31e924e08b75258fa55e829e1a27cf183d45a45d92c7e7f48d1e5591ec158f8a1e5fb3d5037d547e5ae09f7fa4ecdaa75b9b0879647748d70ad942234a2feb82
hints = [0xd2c1d, 0xd2c5d, 0xd2c9d, 0xd2cdd, 0xd6c1d, 0xd6c5d, 0xd6c9d, 0xd6cdd, 0xdac1d, 0xdac5d, 0xdac9d, 0xdacdd, 0xdec1d, 0xdec5d, 0xdec9d, 0xdecdd]
for i in hints:
    assert i & bytes_to_long(b'???') == hints[0]

'''
key = RSA.generate(1024)
n = key.n 
p = key.p
q = key.q
cf = inverse(p,q)
tmp = (1<<22) - 1
p1 = p & tmp
flag = p >> 22
'''

enc_master_key = 0x80e611da674e6654d7aece63cbb659effec7c31739c9e5996ccb6b45d4cb3581b432ac033e6eee900eb30a41ab1964ff52dce8a2c909c1b82a3e102ecc16742cd48d559fdff2372c55d8094913934fcafccdf28bdfd2b081b81dbef2f475e5223e299c623d9f70030a1e288a64978f5c47c022593b70f42dfe2eba90bdb58415
inverse_cf = inverse(cf, n)
PR.<x> = PolynomialRing(Zmod(n))
hint = hints[11]
pol = (x * pow(2,22) + hint)^2 - (x * pow(2,22) + hint) * inverse_cf
pol = pol * inverse(1<<44, n)

dd = pol.degree()
beta = 1                                # b = N
epsilon = beta / 45                # <= beta / 7
mm = ceil(beta**2 / (dd * epsilon))     # optimized value
tt = floor(dd * mm * ((1/beta) - 1))    # optimized value
XX = ceil(n**((beta**2/dd) - epsilon))  # optimized value


start_time = time.time()
roots = coppersmith_howgrave_univariate(pol, n, beta, mm, tt, XX)

print("\n# Solutions")
print("we found:", str(roots))
print("in: %s seconds " % (time.time() - start_time))
print("\n")
p = hints[11] + (2371901149615344640516720542721812092646541458063325759433120180018779229988455585239776007463241636519528075354290515669967446690136059177403229477 << 22)
print(p)
q = n // p
phin = (p-1) * (q-1)
d = inverse(65537, n)
key = RSA.construct((n,65537,d))
cipher = PKCS1_OAEP.new(key)
enc_master_key = bytes_to_long(enc_master_key)
master_key = cipher.decrypt(enc_master_key)
with open('safe.loc', 'rb') as f:
    ciphertext = f.read()
master_cipher = AES.new(master_key, AES.MODE_ECB)
print(master_cipher.decrypt(ciphertext))
