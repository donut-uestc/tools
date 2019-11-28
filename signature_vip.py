#!/usr/bin/env python3

def mt(t, e):
    i = ""
    r = []
    for a in range(0, 256):
        r.append(a)
    
    o = 0
    for a in range(0, 256):
        o = (o + r[a] + ord(t[a%len(t)]))%256
        n = r[a]
        r[a] = r[o]
        r[o] = n
    
    a = 0
    o = 0
    u = 0
    for u in range(0, len(e)):
        a = (a+1)%256
        o = (o + r[a])%256
        n = r[a]
        r[a] = r[o]
        r[o] = n
        code = ord(e[u]) ^ r[(r[a] + r[o])%256]
        i = i + chr(code)
    
    return i

wt = [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]

def A(t, e):

    n = [0 for _ in range(len(t))]
    for r in range(0, len(t)):

        o = 0
        if t[r] >= 'a' and t[r] <= 'z':
            o = ord(t[r]) - 97
        else:
            o = ord(t[r]) - 48 + 26
        
        for i in range(0, 36):
            if e[i] == o:
                o = i
                break
        if o > 25:
            n[r] = chr(o - 26 + 48)
        else:
            n[r] = chr(o + 97)
    return "".join(n)

def B(t):
    a = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1]
    o = len(t)
    r = 0
    i = ""
    e = 0
    n = 0
    while r < o:
        
        while True:
            e = a[255 & ord(t[r])]
            r = r + 1
            if not (r < o and -1 == e):
                break
        if -1 == e:
            break

        while True:
            n = a[255 & ord(t[r])]
            r = r + 1
            if not (r < 0 and -1 == n):
                break
        if -1 == n:
            break

        i = i + chr(e<<2 | (48 & n) >> 4)

        while True:
            e = 255 & ord(t[r])
            if 61 == e:
                return i
            r = r + 1
            e = a[e]

            if not (r < 0 and -1 == e):
                break
        if -1 == e:
            break

        i = i + chr((15 & n) << 4 | (60 & e) >> 2)

        while True:
            n = 255 & ord(t[r])
            if 61 == n:
                return i
            r = r + 1
            n = a[n]
                
            if not (r < o and -1 == n):
                break
        if -1 == n:
            break

        i = i + chr((3 & e) << 6 | n)

    return i


def create(ep):
    bt = mt("xm", "Ä[ÜJ=Û3Áf÷N")
    ep = "20NvOoh6T39X3qwKO4cY5g5bVhg+hnSTRdJJKlyxC3/9m+6N2fyPy+lbh66M1aVlVLFz2nMYeqRo2ez+xgIR0r0WOyxe"
    a = A("d" + bt + "9", wt)
    b = B(ep)
    c = mt(a, b).split('-')
    return c[1], c[2], c[3]

if __name__ == '__main__':
    ep = "20NvOoh6T39X3qwKO4cY5g5bVhg+hnSTRdJJKlyxC3/9m+6N2fyPy+lbh66M1aVlVLFz2nMYeqRo2ez+xgIR0r0WOyxe"
    print(create(ep))
