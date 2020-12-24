#!/usr/bin/env python3

import re
import functools

input = open('day10.txt','r').read().strip()

pos = 0
skip = 0

def knot_hash(knot,lengths,part2=False):
    global pos
    global skip
    if not part2:
        pos = 0
        skip = 0
    for l in [int(s) for s in lengths]:
        if pos+l > len(knot):
            # wrapping around
            el = len(knot)-pos
            bl = l - el
            s = knot[pos:] + knot[:bl]
            rs = s[::-1]
            knot[pos:] = rs[:el]
            knot[:bl] = rs[-bl:]
        else:
            knot[pos:pos+l] = reversed(knot[pos:pos+l])
        pos = (pos + l + skip) % len(knot)
        skip += 1
    return knot

# Part 1
knot = [x for x in range(256)]
lengths = input.split(',')
knot = knot_hash(knot,lengths)
print("Part 1: ",knot[0]*knot[1])

# Part 2
knot = [x for x in range(256)]
lengths = [ord(x) for x in input]
lengths += [17, 31, 73, 47, 23]

pos = 0  # reset our globals
skip = 0
for r in range(64):
    knot = knot_hash(knot,lengths,True)

# compute dense hash by XOR'ing every 16 values
dh = [functools.reduce(lambda x,y:x^y,knot[i:i+16]) for i in range(0,256,16)]
print(dh)
h = ''
# convert to hexadecimal
for d in dh:
    h += "{:02x}".format(d)
assert len(h) == 32
print("Part 2: ",h)
