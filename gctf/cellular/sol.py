import numpy
import os
def bintohex(x):
	tmp = int(x,2)
	return hex(tmp)[2:]
def hextobin(x):
	return bin(x)[2:]

x='66de3c1bf87fdfcf'
def rule(z):
	y=int(z,16)
	x=bin(y)[2:].zfill(64)
	tmp = (3*x)[63:129]
	result = ['1']*64
	for i in range(64):
		if ((tmp[i] == tmp[i+1]) and (tmp[i+1] == tmp[i+2])):
			result[i] = '0'
	result1 = ''.join(result)
	result2 = hex(int(result1,2))[2:]
	if result2[-1:] == 'L':
		result2 = result2[:-1]
	return result2

def reverse(z):
	y=int(z,16)
	x=bin(y)[2:].zfill(64)
	tmp = (3*x)[63:129]
	result = ['']*64
	for i in range(64):
		if(tmp[i+1] == '0'):
			if i != '0':
				result[i] = result[i-1]
		if((tmp[i+1] == '1') and (tmp[i+2] == '0')):
			if i != '0':
				result[i] = str(1-int(result[i-1]))
		if (result[i] == ''):
			result[i] = str(numpy.random.randint(2))
		if(tmp[i+1] == '0'):
			if i != 63:
				result[i+1] = result[i]
		if(tmp[i+1] == '1'):
			if ((i != 0) and (i!=63)) :
				if(result[i] == result[i-1]):
					result[i+1] = str(1-int(result[i]))
	result[63] = result[0]
	result1 = ''.join(result)
	result2 = hex(int(result1,2))[2:]
	if result2[-1:] == 'L':
		result2 = result2[:-1]
	if rule(result2) == z:
		os.system('echo "'+result2+'" > /tmp/plain.key; xxd -r -p /tmp/plain.key > /tmp/enc.key')
		x=os.popen('echo "U2FsdGVkX1/andRK+WVfKqJILMVdx/69xjAzW4KUqsjr98GqzFR793lfNHrw1Blc8UZHWOBrRhtLx3SM38R1MpRegLTHgHzf0EAa3oUeWcQ=" | openssl enc -d -aes-256-cbc -pbkdf2 -md sha1 -base64 --pass file:/tmp/enc.key').read()
		print result2
		return x
	return 0


while(1):
	result=reverse(x)
	if result != 0:
		print result
		if 'CTF' in result:
			print result
			break

#CTF{reversing_cellular_automatas_can_be_done_bit_by_bit}
