from pwn import *
from Crypto.Util.number import *
import string
import hashlib
import itertools
import base64
import json
import random

context.log_level = "error"
def solve_pow(r):
    str_list = (string.ascii_letters+string.digits).encode()
    r.recvuntil('+')
    str_last = r.recvuntil(')')[:-1]
    r.recvuntil('== ')
    hash_value = r.recvline()[:-1]
    r.recvuntil('XXXX:')
    for i in list(itertools.product(str_list, repeat = 4)):
        tmp = bytes(i)
        tmp_str = tmp + str_last
        if (hashlib.sha256(tmp_str).hexdigest()).encode() == hash_value:
            break
    print('get POW')
    return tmp

def set_iv(r):
    r.recvuntil('cmd: ')
    r.sendline('register')
    r.recvuntil('name: ')
    r.sendline('aaaaaaaaaet')
    r.recvuntil('token: ')
    data = json.loads(base64.b64decode(r.recvline()[:-1]).decode())

    encrypted = bytes.fromhex(data['cipher'])
    tmp_encrypted = encrypted[32:]
    tmp = b'who": "user", "n'
    tmp1 = b'{"' + random.choice(string.ascii_letters).encode() + b'": "user", "n'
    iv = long_to_bytes(bytes_to_long(tmp) ^ bytes_to_long(tmp1) ^ bytes_to_long(encrypted[16:32]))
    data['cipher'] = tmp_encrypted.hex()
    data['iv'] = iv.hex()

    token = base64.b64encode(json.dumps(data).encode()).decode()
    r.recvuntil('cmd: ')
    r.sendline('login')
    r.recvuntil('token: ')
    r.sendline(token)
    print('set iv')
    return data['iv'], token

def get_user(iv, enc):
    data = {'iv' : iv, 'cipher' : enc}
    token = base64.b64encode(json.dumps(data).encode()).decode()
    r = remote('54.178.3.192', 9427)
    r.sendline(solve_pow(r))
    r.recvuntil('cmd: ')
    r.sendline('login')
    r.recvuntil('token: ')
    r.sendline(token)
    try:
        r.recv()
        r.close()
        return True
    except:
        r.close()
        return False



r = remote('54.178.3.192', 9427)
r.sendline(solve_pow(r))
r.recvuntil('cmd: ')
r.sendline('register')
r.recvuntil('name: ')
r.sendline('a'*9 + 'a'*16)
r.recvuntil('token: ')
data = json.loads(base64.b64decode(r.recvline()[:-1]).decode())
encrypted = bytes.fromhex(data['cipher'])
iv = encrypted[:16]
token = encrypted[16:]
print(iv.hex())
print(token.hex())

iv = bytes.fromhex('bc9a989f4a4a8bf92a726a70fd0a4618')
enc = bytes.fromhex('58840fff950d70f357aa103f579119d12f33725acb0963bb40a9fd005ff154437fbeea56f5ba7cb461acf9430910c6463454fd4315cf10b2c4736c1c71b02e8553b6e63dcc4ff6bbae0be04eedaf4d4c')

enc1 = enc[:16]
enc2 = enc[16:]
iv_list = list(iv)
iv_list[0] = ord(b'o') ^ ord(b'{') ^ iv_list[0]
iv_list[1] = ord(b'n') ^ ord(b'"') ^ iv_list[1]
iv_list[12] = ord(b'"') ^ ord(b'a') ^ iv_list[12]
iv_list[15] = ord(b'"') ^ ord(b'a') ^ iv_list[15]

#ord(b'\\') = 0x62
#ord(b'""') = 0x22
for i in range(49,122):
    print(hex(i))
    iv_list[5] = i ^ ord(b'"') ^ iv_list[5]
    if get_user(bytes(iv_list).hex(), enc.hex()) == False:
        print('find candidate')
        print(chr(i))
    iv_list[5] = i ^ ord(b'"') ^ iv_list[5]


#hitcon{JSON_is_5

 #get data
'''
for i in range(0,13):
    r = remote('54.178.3.192', 9427)
    r.sendline(solve_pow(r))
    iv, token = set_iv(r)
    r.recvuntil('cmd: ')
    r.sendline('register')
    r.recvuntil('name: ')
    r.sendline('a' * (9+16*10000000))
    r.recvuntil('token: ')
    data = json.loads(base64.b64decode(r.recvline()[:-1]).decode())
    with open('data'+str(i),'w') as f:
        f.write(iv + '\n')
        f.write(token + '\n')
        f.write(data['cipher'])
    r.close()
'''
'''
r = remote('54.178.3.192', 9427)
r.sendline(solve_pow(r))
r.recvuntil('cmd: ')
r.sendline('login')
r.recvuntil('token: ')
r.sendline('eyJjaXBoZXIiOiAiOGE5YWJmZjQwZTcwMzYzMmFjYmQ1M2FmOTQ1MjEwYjYzYTJlZmI1ZTRmZWY0ZDVlNzI5NWJiN2EwMWIzYWQwYTc4MTU0MmJkODExMjQ0NjNiNmVmYzk5NTQzZjFhMWZiIiwgIml2IjogIjNiYmYwYTUzNjUyZjkxMWIwODcxM2YwMzk4NGI5ZTMxIn0=')
r.recvuntil('cmd: ')
r.sendline('register')
r.recvuntil('name: ')
r.sendline('a' * (9+16*2576832) + '{z2_[cEeb?$3xjgR')
r.recvuntil('token: ')
data = json.loads(base64.b64decode(r.recvline()[:-1]).decode())
with open('data','w') as f:
    f.write(data['cipher'])
r.close()
'''

#admin secret cipher
'''
string1 = '{"cmd":"get_secret","who":"admin","alpha":"aaa","name":"admin"}'
cipher = 'caa75b43bb137f370909919d09323aa9ddca908e6f57eaf87302398e3c7dbd99dc6116f323d7a22c862207df113ba918af00ab30408cee3df584bdca11d62b3f'
data = {}
data['cipher'] = cipher
data['iv'] = '3ba973174ff4a231b2bc9e9ef3a03efe'
token = base64.b64encode(json.dumps(data).encode()).decode()
r = remote('54.178.3.192', 9427)
r.sendline(solve_pow(r))
r.recvuntil('cmd: ')
r.sendline('login')
r.recvuntil('token: ')
r.sendline(token)
r.interactive()
'''
'''
cipher = 'caa75b43bb137f370909919d09323aa9ddca908e6f57eaf87302398e3c7dbd99dc6116f323d7a22c862207df113ba918ff95b8e2e1b1b5ae6faf4a9166c7a74a1417d49cc4390130384965eb58051a9c'
data = {}
data['cipher'] = cipher
data['iv'] = '3ba973174ff4a231b2bc9e9ef3a03efe'
token = base64.b64encode(json.dumps(data).encode()).decode()
r = remote('54.178.3.192', 9427)
r.sendline(solve_pow(r))
r.recvuntil('cmd: ')
r.sendline('login')
r.recvuntil('token: ')
r.sendline(token)
r.interactive()


'''


