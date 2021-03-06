from Crypto.Util.number import *
from Crypto.Cipher import AES
import hashlib
with open('output', 'r') as f:
    output_arr = eval(f.readline()[:-1])

n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
'''
M = matrix(QQ,62)
B = getRandomNBitInteger(41)
print(B)
for i in range(30):
    M[i,i] = n
    M[30+i, i] = 1 << 216
    M[30+i, 30+i] = -1
    h = output_arr[i][0]
    lea_k = output_arr[i][1] << 40
    r = output_arr[i][2]
    s = output_arr[i][3]
    M[60, i] = -r * inverse(s, n) % n
    M[61, i] = (lea_k - h * inverse(s, n)) % n

M[60, 60] = B / n
M[61, 61] = B
M = M.LLL()
print(n + M[1][60] * n / B)
print(M[1][61])
'''

secret = 86829171062216374641826382742719750658329979820493055287648665496168943473403
enc_flag = '8d47217b47714708b39befc5bef252e621d3c10fdb1d8d6168c62c4f7b981c185b44a907c9db378b1bfd3b984262ad157ead801493286eb877e7c774978c3f4d'
sha256 = hashlib.sha256()
sha256.update(str(secret).encode())
key = sha256.digest()

aes = AES.new(key, mode=AES.MODE_ECB)
print(aes.decrypt(bytes.fromhex(enc_flag)))
#pbctf{!!!_https://eprint.iacr.org/2019/023.pdf_$$$}