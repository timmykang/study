import cipher
def log2(x):
	i=0
	while(x!=1):
		i=i+1
		if x%2 == 1:
			print 'error'
			break
		x=x/2
	return i
data=[]
data1= 0
for i in cipher.x:
	data.append(log2(i))
encflag = data[12:]+data[:12]
flag =''
for i in encflag:
	flag = flag + chr(i+60)
print flag
print encflag
print data
