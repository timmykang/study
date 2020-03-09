from crypto_2 import *

def get_temp(self, salt = None, tmp = 0):
    temp = copy.copy(self.rotor)
    if salt is not None:
        temp = self.handle_salt(salt, self.b, temp, RATE)
    temp[4] = temp[4] - 1 if temp[4] & 1 else temp[4] + 1
    for i in range(tmp):
        self.black_box(temp, self.c)
    return temp

abcd = 0
salt_bytes = b'once_upon_a_time'
plain = 'timmykan'.encode()
encflag = '3bb0c885fe4b717825546c6ccbcab27386e35f0e44ee25e7b339f3c0000000000000000000000000'

while(True):
    tmp = abcd
    d = tmp % 32; tmp = tmp // 32
    c = tmp % 32; tmp = tmp // 32
    b = tmp % 32; tmp = tmp // 32
    a = tmp % 32
    server = TheOracle(b'this_is_timmykang', b'do_not_roll_your_own_crypto')
    server.a = a; server.b = b; server.c = c; server.d = d
    server.rotor = list()
    server.init_rotor()
    cipher = server.encrypt(salt_bytes, plain)
    if(cipher == encflag[:16]):
        break
    abcd += 1
    print(abcd)

flag =''

temp = get_temp(server, salt_bytes, 0)[0]
flag1 = (temp^int(encflag[0:16],16))
temp = get_temp(server, salt_bytes, 1)[0]
flag2 = (temp^ flag1 ^ int(encflag[16:32],16))
temp = get_temp(server, salt_bytes, 2)[0]
flag3 = temp ^ flag1 ^ flag2 ^ int(encflag[32:48],16)
temp = get_temp(server, salt_bytes, 3)[0]
flag4 = temp ^ flag1 ^ flag2 ^ flag3 ^ int(encflag[48:64],16)
flag = hex(flag1) + hex(flag2)[2:] + hex(flag3)[2:] + hex(flag4)[2:]
print(bytes.fromhex(flag[2:58]).decode('utf-8'))

#timmykang{EZ_CRYPTO_PROBLEM}