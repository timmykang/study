from Crypto.Util.number import *
import pickle
import os, sys
import string, random
from hashlib import sha256
from pwn import *
tbits = 512
gbits = 64
r=remote('192.168.10.52',18181)
r.recvuntil(': ')
alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
proof_prefix = r.recvline()[:-1]
r.recvuntil(': ')
proof_hash = r.recvline()[:-1]
r.recvuntil(': ')
#proof_prefix = 'tI0ln1JePyG2'
#proof_hash = '542f0730552821bc1bd225b3a64a9d97b52ec68d0f5227a1a1ecdd744fe7f074'
flag = 0
for i1 in alphabet:
	for i2 in alphabet:
		for i3 in alphabet:
			for i4 in alphabet:
				proof = i1+i2+i3+i4
				tmp = proof_prefix+proof
				if(sha256(tmp.encode()).hexdigest()==proof_hash):
					flag = 1
					print proof
					break
			if(flag == 1):
				break
		if(flag == 1):
			break
	if(flag == 1):
		break
r.send(proof+'\n')
r.recvuntil('= ')
print 'N'
print r.recvline()
r.recvuntil('= ')
r.recvuntil('= ')
print 'flag'
print r.recvline()
r.recvuntil('> ')
r.send('cc1e3e439d770d7c96e0020ddd5233f3ded56bca3e33bc49d95514242f5e53cd707e6c6061e1fae8a80c7b9569140cd059b326287a0f6101e861367775be28dafe9c2cfc9bd2b0816de05f3493377eb885e30e25394610b258e5b229283965532114641b6cfdd3d0d89d190aa3007a2d9afee21e354f41aee412d775d64f42489bc8ceee4670b5d4e40723733add7c294a077bd99cd268001e62175a34f8b5addc8a42672299055f288b03f54291c1bff3be0130900178e1de0d7a08c2e6f5ff2f569fec65a861263e843b7602d82fa3e9a4d8e8bead1768bd4c5f66506ac941332882951e0a1abe5b092d2e012ef399baf587a60981e7d4826bd5974010612678e2a8cc024ad028f4703379a36e1ea67a0cae233f7e59c46e25ae38588fe49c08757f67f8e578534c6ac7b5150d381d6cf57814104f0da24f056c60954e757e5914508e88c7d1120f9d7ec163f5b12f501af3841d6092c031ddd3748cef1559c04cf32a6c86586170334018106a64b85e8a6f7ece656761052226c195a4ca3740d39447304856f45b066b3bb61aa8546c3482169beb1f34de5f626bb88f47dda4332d0a4587102f256a92b3880df2c1b861fb62098ca9c7e477440f0ec2550d71b9f29f1628fb8a35ba1be7ef5c0e4d3469387357211b79babe16a653b01bd5f017090212b5d44ff419aeee746e23f95598bd6daa020b708fde8f2d4a0526a122c6f189d588765ae8150f429b3922c18a2cb025aaee26418b8073d1a4fc81659196141b2209d09315a16c172f0d094e033aa20be4e900ca230582577d997787\n')
r.recvuntil('p: ')
print 'part p'
print r.recvline()
