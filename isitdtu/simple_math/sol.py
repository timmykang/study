from pwn import *
def shiftdigit(x,i):
	y=[]
	for j in x:
		y.append(j[i:])
	return y
	
def checkone(x):
	i=0
	if x[0][5] != '#':
		if x[1][5] != '#':
			if x[2][5] != '#':
				if x[3][5] != '#':
					if x[4][5] != '#':
						if x[5][5] != '#':
							if x[6][5] != '#':
								i=1
	return i
def checknum(x):
	i=0
	if x[0][0] != '#':
		if x[0][2] != '#':
			i=1
	return i

def findcalc(x):
	if x[1][2] == '#':
		return '+'
	elif x[1][1] =='#':
		return '*'
	else:
		return '-'
def findnum(x):
	if x[0][2] != '#':
		return 4
	elif x[0][1] != '#':
		return 0
	elif x[0][0] != '#':
		if x[2][0] != '#':
			if x[4][0] != '#':
				return 3
			else:
				return 2
		else:
			if x[3][0] == '#':
				return 6
			elif x[4][0] == '#':
				return 8
			else:
				return 9
	else:
		if x[2][0] == '#':
			return 5
		else:
			return 7

r=remote('104.154.120.223', 8083)
time = 0
for xxx in range(100):
	time = time +1
	print time
	calc = ''
	x=[]
	print r.recvline()
	for i in range(7):
		tmp = r.recvline()[:-1]
		print tmp
		x.append(tmp)
	print r.recvline()
	if checkone(x) == 1:
		calc = calc+'1'
		x=shiftdigit(x,6)
	else:
		calc = calc+str(findnum(x))
		x=shiftdigit(x,8)
	if checknum(x) == 1:
		tmp0 = findcalc(x)
		if tmp0 == '*':
			x=shiftdigit(x,8)
		else:
			x=shiftdigit(x,6)
		calc = calc+tmp0
	else:
		if checkone(x) == 1:
			calc = calc+'1'
			x=shiftdigit(x,6)
		else:
			calc = calc+str(findnum(x))
			x=shiftdigit(x,8)
		tmp0 = findcalc(x)
		#print tmp0
		if tmp0 == '*':
			x=shiftdigit(x,8)
		else:
			x=shiftdigit(x,6)
		calc = calc+tmp0
	if checkone(x) == 1:
		calc = calc+'1'
		x=shiftdigit(x,6)
	else:
		calc = calc+str(findnum(x))
		x=shiftdigit(x,8)
	#print calc
	if checknum(x) == 0:
		if checkone(x) == 1:
			calc = calc+'1'
			x=shiftdigit(x,6)
		else:
			calc = calc+str(findnum(x))
			x=shiftdigit(x,8)
	#print calc
	ans=eval(calc)
	print r.recvuntil('> ')
	print ans
	r.send(str(ans)+'\n')

print r.recv()
r.close()
#ISITDTU{sub5cr1b3_b4_t4n_vl0g_4nd_p3wd13p13}




