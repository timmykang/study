from Crypto.Util.number import *
Ptmp = '00:ad:87:f0:86:a4:e1:ac:d2:55:d1:d7:73:24:a0:5e:a7:d2:50:f2:85:f3:a6:de:35:b9:f0:7c:5d:08:3a:dd:51:66:67:74:25:b8:33:53:28:25:5e:7b:56:2f:94:4d:55:c5:6f:f0:84:f4:31:6f:dc:9e:3f:5b:00:9f:ef:d6:50:15:a5:ca:22:8c:94:e3:fd:35:c6:ab:a8:3e:a4:e2:08:00:a3:45:48:aa:36:a5:d4:0e:3c:74:96:c6:5b:db:c8:64:e8:f1:61'
P = ''
for i in range(len(Ptmp)):
	if(i%3 != 2):
		P = P+Ptmp[i]
print isPrime(int(P,16))

