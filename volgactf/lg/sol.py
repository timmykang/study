from pwn import *
def GCD(x, y): 
  
   while(y): 
       x, y = y, x % y 
  
   return x 
r=remote("lg.q.2019.volgactf.ru",8801)
r.recvuntil(":\n")
x=[]
y=[]
x.append(r.recvuntil("\n")[:-1])
x.append(r.recvuntil("\n")[:-1])
x.append(r.recvuntil("\n")[:-1])
x.append(r.recvuntil("\n")[:-1])
x.append(r.recvuntil("\n")[:-1])
x.append(r.recvuntil("\n")[:-1])
x.append(r.recvuntil("\n")[:-1])
for i in x:
		y.append(int(i))
r.recvuntil(">>>")
key='-1'
for i in range(6):
	print GCD(y[i],y[i+1])
r.send(key+'\n')
print r.recv()
r.close()
