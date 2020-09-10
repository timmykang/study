import gensafeprime
from Crypto.Util.number import bytes_to_long
with open('flag.txt', 'rb') as f:
    flag = f.read().strip()
n = ZZ(bytes_to_long(flag))

p = gensafeprime.generate(n.nbits() + 1)
assert n < p
print('p =', p)

K = Zmod(p)

def hash_with_params(g, h, a1, a0):
    def step(prev1, prev2):
        return vector([g * prev1 - h * prev2, prev1])
    def steps(n):
        Kx.<prev1, prev2> = K[]
        if n == 0: return vector([prev1, prev2])
        half = steps(n // 2)
        full = half(*half)
        if n % 2 == 0: return full
        else: return step(*full)
    return steps(n)[0](a1, a0)

print(hash_with_params(6, 9,   3141592653589793, 2384626433832795))
print(hash_with_params(8, 15,   288419716939937, 5105820974944592))
print(hash_with_params(10, 21, 3078164062862089, 9862803482534211))
print(hash_with_params(12, 35, 7067982148086513, 2823066470938446))

