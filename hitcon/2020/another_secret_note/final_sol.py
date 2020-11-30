from pwn import *
from Crypto.Util.number import *
import string
import hashlib
import itertools
import base64
import json
import random
context.log_level = "error"

string1 = '{"cmd":"get_secret","who":"admin","alpha":"aaa","name":"admin"}'
data = json.loads(string1)
data["secret"] = 'asdfasdfasdfasdf'
data_str = json.dumps(data)
token = 'eyJjaXBoZXIiOiAiZmYxY2RhY2Y5ZWNjMGM5YzgxMDk1NWViYWU0OGIyN2EzOTg4MDYxNmFlMTUwZGNhYzY4NWMwMmJkOWFhMmZkMjVhZGZmYjIzOGJiMDU2ZWIwMjc5ZWUwYmU2YjUxMTkyOWExZDM0YTk3YTQ2YzMyM2QxMGQxYmI0MDdkMmM2YjMzZjYyMGUxMmIwOTkzZmQ5MzRmOWEwYWQ4ZjlkYjVkYTgzYzAwNDkwMmMxZDM5MDViZWVlNjJmZTNkZmFiNjE0Y2U0ZDUxZTA5OTdkYzM1YmZhOGY0YTc5Y2FjMGUxOTkifQ=='
enc_token = (json.loads(base64.b64decode(token.encode()).decode()))
cipher = bytes.fromhex(enc_token['cipher'])
print(data_str[80:96].encode())
string1 = '{"cmd":"get_secret","who":"admin","alpha":"aaa","name":"admin","a":"aaa"}'
data = json.loads(string1)
data["secret"] = 'asdfasdfasdfasdf'
data_str = json.dumps(data)
token = 'eyJjaXBoZXIiOiAiZmYxY2RhY2Y5ZWNjMGM5YzgxMDk1NWViYWU0OGIyN2EzOTg4MDYxNmFlMTUwZGNhYzY4NWMwMmJkOWFhMmZkMjVhZGZmYjIzOGJiMDU2ZWIwMjc5ZWUwYmU2YjUxMTkyOWExZDM0YTk3YTQ2YzMyM2QxMGQxYmI0MDdkMmM2YjM4OTU5YzA4OTk0YzVjY2Q0YjE4M2Q3MGRkZTFmOTUzM2JhZjZjYThmZmE0MGRjNzVhZWIzM2RlOTk5OWVmNDhmOTBjMmQ1MGQ5MzFhMDU2YmVlNDNlZWU3YzkyYWY4OTQ4MWRhYzdmZjlkMzdlNTg1ODI2MmM5NTcxYjFhM2ZmZSJ9'
enc_token = (json.loads(base64.b64decode(token.encode()).decode()))
cipher = bytes.fromhex(enc_token['cipher'])
print(data_str[80:96].encode())

string1 = '{"cmd":"get_secret","who":"admin","alpha":"aaa","name":"admin","a":"a"}'
data = json.loads(string1)
data["secret"] = 'asdfasdfasdfasdf'
data_str = json.dumps(data)
token = 'eyJjaXBoZXIiOiAiZmYxY2RhY2Y5ZWNjMGM5YzgxMDk1NWViYWU0OGIyN2EzOTg4MDYxNmFlMTUwZGNhYzY4NWMwMmJkOWFhMmZkMjVhZGZmYjIzOGJiMDU2ZWIwMjc5ZWUwYmU2YjUxMTkyOWExZDM0YTk3YTQ2YzMyM2QxMGQxYmI0MDdkMmM2YjM2MGE2NzRhYWNhZmQ1M2QxZDI2MjUzNDNlMTgzNjkyMmIzN2I3NWI1ODVhYzY5YjFhN2EyMzliM2Q4Y2IwZDM1NDc0NDQxNDA0MmViYmU2NGE1YmVkOTdhZTFiNTk3MTkifQ=='
enc_token = (json.loads(base64.b64decode(token.encode()).decode()))
cipher = bytes.fromhex(enc_token['cipher'])

print(data_str[96:112].encode())

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

def get_user(iv, enc):
    data = {'iv' : iv, 'cipher' : enc}
    token = base64.b64encode(json.dumps(data).encode()).decode()
    #r = process('./prob1.py')
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

enc = cipher[96:]
iv_list = list(cipher[80:96])
tmp_flag = b'woNderFul!@##}"}'
target =   b'{              }'
'''
for i in range(16):
    iv_list[i] = (tmp_flag[i]) ^ (target[i]) ^ iv_list[i]
print((get_user(bytes(iv_list).hex(), enc.hex())))

for i in range(33,122):
    print(hex(i))
    iv_list[-5] = i ^ ord(b'\\') ^ iv_list[-5]
    if (get_user(bytes(iv_list).hex(), enc.hex())) == False:
        print('find candidate')
        print(chr(i))
    iv_list[-5] = i ^ ord(b'\\') ^ iv_list[-5]

'''
#hitcon{JSON_is_50_woNderFul!@##}

enc = bytes.fromhex('53db0d62abb57fd568b074736613c62537c18020855cad1ebc9e4de1ee3884fd44f299403f509d022b73b681e0c28b12e59d8599d6fe8accefb6c97396c748e7ee418c569a6cbca9fd572f845f42d35a')
iv_list = list(bytes.fromhex('9934daf56ad2f54ed73db631c2cb52ce'))

iv_list[0] = ord(b'o') ^ ord(b'{') ^ iv_list[0]
iv_list[1] = ord(b'n') ^ ord(b'"') ^ iv_list[1]
iv_list[12] = ord(b'"') ^ ord(b'a') ^ iv_list[12]
iv_list[15] = ord(b'"') ^ ord(b'a') ^ iv_list[15]

for i in range(83,122):
    print(hex(i))
    iv_list[4] = i ^ ord(b'"') ^ iv_list[4]
    if (get_user(bytes(iv_list).hex(), enc.hex())) == False:
        print('find candidate')
        print(chr(i))
    iv_list[4] = i ^ ord(b'"') ^ iv_list[4]