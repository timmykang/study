from pwn import *
r=remote('34.68.81.63', 6666)
time = 0
for i in range(50):
	time = time +1
	print time
	print r.recvuntil('Weighting 1: ')
	r.send('1,2,3,4 5,6,7,8\n')
	x=r.recvline()[:-1]
	#print x
	if x == 'Both are equally heavy':
		r.recvuntil('Weighting 2: ')
		r.send('6,7,8 9,10,11\n')
		x1=r.recvline()[:-1]
		if x1 == 'Both are equally heavy':
			r.recvuntil('Weighting 3: ')
			r.send('11 12\n')
			x=r.recvline()[:-1]
			r.recvline()
			r.send('12\n')
		elif 'lighter' in x1:
			r.recvuntil('Weighting 3: ')
			r.send('9 10\n')
			x=r.recvline()[:-1]
			r.recvline()
			if 'equal' in x:
				r.send('11\n')
			elif 'light' in x:
				r.send('10\n')
			else:
				r.send('9\n')
		else:
			r.recvuntil('Weighting 3: ')
			r.send('9 10\n')
			x=r.recvline()[:-1]
			if 'equal' in x:
				r.send('11\n')
			elif 'light' in x:
				r.send('9\n')
			else:
				r.send('10\n')
	elif 'light' in x:
		r.recvuntil('Weighting 2: ')
		r.send('1,2,5 3,6,12\n')
		x=r.recvline()[:-1]
		if 'equal' in x:
			r.recvuntil('Weighting 3: ')
			r.send('7 8\n')
			x=r.recvline()[:-1]
			r.recvline()
			if 'equal' in x:
				r.send('4\n')
			elif 'light' in x:
				r.send('8\n')
			else:
				r.send('7\n')
		elif 'light' in x:
			r.recvuntil('Weighting 3: ')
			r.send('1 2\n')
			x=r.recvline()[:-1]
			r.recvline()
			if 'equal' in x:
				r.send('6\n')
			elif 'light' in x:
				r.send('1\n')
			else:
				r.send('2\n')
		else:
			r.recvuntil('Weighting 3: ')
			r.send('5 1\n')
			x=r.recvline()[:-1]
			r.recvline()
			if 'equal' in x:
				r.send('3\n')
			elif 'light' in x:
				r.send('5\n')
			else:
				r.send('5\n')
	else:
		r.recvuntil('Weighting 2: ')
		r.send('1,5,6 2,7,12\n')
		x=r.recvline()[:-1]
		if 'equal' in x:
			r.recvuntil('Weighting 3: ')
			r.send('3 4\n')
			x=r.recvline()[:-1]
			r.recvline()
			if 'equal' in x:
				r.send('8\n')
			elif 'light' in x:
				r.send('4\n')
			else:
				r.send('3\n')
		elif 'light' in x:
			r.recvuntil('Weighting 3: ')
			r.send('5 6\n')
			x=r.recvline()[:-1]
			r.recvline()
			if 'equal' in x:
				r.send('2\n')
			elif 'light' in x:
				r.send('5\n')
			else:
				r.send('6\n')
		else:
			r.recvuntil('Weighting 3: ')
			r.send('7 12\n')
			x=r.recvline()[:-1]
			r.recvline()
			if 'equal' in x:
				r.send('1\n')
			elif 'light' in x:
				r.send('7\n')
			else:
				r.send('7\n')
	print r.recvline()

print r.recv()
#ISITDTU{y0u_hav3_200iq!!!!}
		
r.close()

