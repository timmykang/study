def egcd(a1, a2):
    x1, x2 = 1, 0
    y1, y2 = 0, 1
    while a2:
        print (x1,y1,a1)
        q = a1 // a2
        a1, a2 = a2, a1 - q * a2
        x1, x2 = x2, x1 - q * x2
        y1, y2 = y2, y1 - q * y2
    return (x1, y1, a1)

print egcd(15,18)
print egcd(28382,12959)
