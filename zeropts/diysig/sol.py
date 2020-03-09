from pwn import *
from Crypto.Util.number import *
n = int('6d70b5a586fcc4135f0c590e470c8d6758ce47ce88263ff4d4cf49163457c71e944e9da2b20c2ccb0936360f12c07df7e7e80cd1f38f2c449aad8adaa5c6e3d51f15878f456ceee4f61547302960d9d6a5bdfad136ed0eb7691358d36ae93aeb300c260e512faefe5cc0f41c546b959082b4714f05339621b225608da849c30f',16)
enc = int('3cfa0e6ea76e899f86f9a8b50fd6e76731ca5528d59f074491ef7a6271513b2f202f4777f48a349944746e97b9e8a4521a52c86ef20e9ea354c0261ed7d73fc4ce5002c45e7b0481bb8cbe6ce1f9ef8228351dd7daa13ccc1e3febd11e8df1a99303fd2a2f789772f64cbdb847d6544393e53eee20f3076d6cdb484094ceb5c1',16)
e = 0x10001
sig1 = 0x3b71ec3d
def getsig(x):
    r=remote('18.179.178.246',3001)
    r.recvuntil('> ')
    r.send('2\n')
    r.recvuntil(': ')
    tmp = hex(x)[2:]
    r.send(tmp+'\n')
    r.recvuntil(': ')
    r.send('\n')
    r.recvuntil('= ')
    ret = r.recvuntil('\n')[:-1]
    r.close()
    return int(ret,16)%2

big = (n)
small = (0)
tmp1 = (n)

for i in range(700):
    tmp1 = tmp1 / 2
    big = big - int(tmp1)

for i in range(700,1024):
    tmp1 = (tmp1) /2
    tmp = pow(2,e*(i+1),n)
    if getsig((tmp*enc)%n) == 1:
        small = small + int(tmp1)
    else:
        big = big - int(tmp1)


print hex(big) #0x7a6572307074737b6e337633725f72337633346c5f3768335f4c53443f
print hex(small) #0x7a6572307074737b6e337633725f72337633346c5f3768335f4c534247
last_byte = '}'
flag1 = 0x7a6572307074737b6e337633725f72337633346c5f3768335f4c53437d
flag2 = 0x7a6572307074737b6e337633725f72337633346c5f3768335f4c53427d
print long_to_bytes(flag1)
print long_to_bytes(flag2)

#zer0pts{n3v3r_r3v34l_7h3_LSB}
