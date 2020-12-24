#!/usr/bin/env python3

seedA = 277
seedB = 349

#seedA = 65   # sample
#seedB = 8921

def genA(P2=False):
    factor = 16807
    prev = seedA
    while True:
        next_val = (prev * factor) % 2147483647
        valb = bin(next_val)
        prev = next_val
        if P2 and valb[-2:] != '00': # div by 4?
            continue
        yield valb


def genB(P2=False):
    factor = 48271
    prev = seedB
    while True:
        next_val = (prev * factor) % 2147483647
        valb = bin(next_val)
        prev = next_val
        if P2 and valb[-3:] != '000': # div by 8?
            continue
        yield valb


A = genA()
B = genB()
pairs = 0
for _ in range(40000000):
    a,b = next(A),next(B)
    if a[-16:] == b[-16:]:
        pairs += 1
print(pairs)

A = genA(True)
B = genB(True)
pairs = 0
for _ in range(5000000):
    a,b = next(A),next(B)
    if a[-16:] == b[-16:]:
        pairs += 1
print(pairs)
