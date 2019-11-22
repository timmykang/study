from pwn import *
from Crypto.Util.number import *
import sys
import struct
import hashlib
import primelist
from wiener import wiener

def pow_hash(challenge, solution):
    return hashlib.sha256(challenge.encode('ascii') + struct.pack('<Q', solution)).hexdigest()

def check_pow(challenge, n, solution):
    h = pow_hash(challenge, solution)
    return (int(h, 16) % (2**n)) == 0

def solve_pow(challenge, n):
    candidate = 0
    while True:
        if check_pow(challenge, n, candidate):
            return candidate
        candidate += 1
def funA():
	r = remote("asrybab.quals2019.oooverflow.io",1280)
	r.recvuntil('Challenge: ')
	challenge=r.recvline()[:-1]
	r.recvuntil('n: ')
	n=int(r.recvline()[:-1])
	r.recvline()
	solution = solve_pow(challenge,n)
	r.send(str(solution)+'\n')
	r.recvline()
	r.send('\n')
	r.recvline()
	r.recvline()
	return r

def fun1():
	challenge=[]
	nev=[]
	r=funA()
	r.send('1\n')
	nev.append(int(r.recvline()[:-1]))
	nev.append(int(r.recvline()[:-1]))
	nev.append(int(r.recvline()[:-1]))
	challenge.append(nev)
	nev=[]
	nev.append(int(r.recvline()[:-1]))
	nev.append(int(r.recvline()[:-1]))
	nev.append(int(r.recvline()[:-1]))
	challenge.append(nev)
	nev=[]
	nev.append(int(r.recvline()[:-1]))
	nev.append(int(r.recvline()[:-1]))
	nev.append(int(r.recvline()[:-1]))
	challenge.append(nev)
	ctime = int(r.recvline()[:-1])
	hm = r.recvline()[:-1]
	r.close()
	return challenge, ctime, hm

def fun2(challenge,ctime,hm):
	r=funA()
	r.send('2\n')
	r.send('11\n')
	r.send('11\n')
	r.send('11\n')
	for i in range(9):
		r.send(str(challenge[i/3][i%3])+'\n')
	r.send(str(ctime)+'\n')
	r.send(hm+'\n')
	print r.recvline()
	print r.recvline()
	r.close()
n = 744818955050534464823866087257532356968231824820271085207879949998948199709147121321290553099733152323288251591199926821010868081248668951049658913424473469563234265317502534369961636698778949885321284313747952124526309774208636874553139856631170172521493735303157992414728027248540362231668996541750186125327789044965306612074232604373780686285181122911537441192943073310204209086616936360770367059427862743272542535703406418700365566693954029683680217414854103

e = 57595780582988797422250554495450258341283036312290233089677435648298040662780680840440367886540630330262961400339569961467848933132138886193931053170732881768402173651699826215256813839287157821765771634896183026173084615451076310999329120859080878365701402596570941770905755711526708704996817430012923885310126572767854017353205940605301573014555030099067727738540219598443066483590687404131524809345134371422575152698769519371943813733026109708642159828957941

challenge, ctime, hm = fun1()
print "nev = ", challenge
print "ctime = ", ctime 
print 'hm = ', hm

'''while(1):
	challenge, ctime, hm = fun1()
	for i in range(3):
		print i
		for j in primelist.y:
			n=challenge[i][0]
			e=challenge[i][1]*j
			if wiener(n,e) != -1:
				print n
				print e
				print challenge, ctime, hm'''
