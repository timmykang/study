from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
f= open('pub.der','r')
pkey = RSA.importKey(f.read())
print AES.block_size
print len(hex(pkey.n)[2:])
print hex(pkey.n)
print hex(pkey.e)
f.close()
