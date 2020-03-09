from pwn import *
from Crypto.Util.number import *
import base64
r=remote('13.231.224.102',3002)
r.recvuntil('[')
x=[]
x.append(eval(r.recvuntil(']')))
for i in range(5):
    r.recvuntil('\n')
    x.append(eval(r.recvuntil(']')))
r.recvuntil('= ')
p=int(r.recvuntil('\n')[:-1])
data = []

for i in range(64):
    tmp = [[0 for j in range(6)] for i in range(6)]
    for j in range(6):
        for k in range(6):
            tmp[j][k] = x[j][k] % 256
            x[j][k] = x[j][k] // 256
    data.append(tmp)

def make_mes(mes):
    send_mes = ''
    for i in range(6):
        for j in range(6):
            send_mes = send_mes + long_to_bytes(mes[i][j])
    return_mes = base64.b64encode(send_mes)
    return return_mes

def recv_matrix(r):
    r.recvuntil('[')
    tmp_x=[]
    tmp_x.append(eval(r.recvuntil(']')))
    for i in range(5):
        r.recvuntil('\n')
        tmp_x.append(eval(r.recvuntil(']')))
    return tmp_x

for i in range(64):
    print(i)
    r.recvuntil('>')
    r.send('2\n')
    mes = make_mes(data[i])
    r.send(mes+'\n')
    tmp = recv_matrix(r)
    for j in range(6):
        for k in range(6):
            x[j][k] = (x[j][k] + pow(256,i) * tmp[j][k]) % p
flag = ''
for i in range(6):
    for j in range(6):
        flag = flag + long_to_bytes(x[i][j])
print flag
#zer0pts{r1ng_h0m0m0rph1sm_1s_c00l}



