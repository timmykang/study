import os


def keysched():
    key = os.urandom(32)
    keylength = len(key)
    s = list(range(256))
    j = 0

    for i, s_i in enumerate(s):
        j = (j + s_i + key[i % keylength]) % 255
        s[i], s[j] = s[j], s[i]

    return 0, 0, s


def encrypt(plaintext, sbox):
    i, j, s = sbox
    ciphertext = []

    for pt in plaintext:
        i = (i + 1) % 255
        j = (j + s[i]) % 255
        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) % 255]
        ciphertext.append(bytes([k ^ pt]))

    return b"".join(ciphertext), (i, j, s)


def main():
    plaintext = ""
    s = keysched()

    print("type 'source' for source")
    while True:
        cmd = input("> ")
        if cmd == "source":
            with open(__file__, "r") as srcf:
                print(srcf.read())
        elif cmd == "read":
            with open("flag.txt", "rb") as flagf:
                flag = flagf.read().strip()
            plaintext = (flag * 2500)[:100000]
        elif cmd == "reload":
            s = keysched()
        elif cmd.startswith("encrypt "):
            length = int(cmd.split(" ")[1])
            ct, s = encrypt(plaintext[:length], s)
            plaintext = plaintext[length:]
            print(ct.hex())
        elif cmd == "exit":
            break


if __name__ == "__main__":
    main()