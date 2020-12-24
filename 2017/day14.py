#!/usr/bin/env python3

import re
import functools
import collections


key = 'hfdlxzhv' # input
#key = 'flqrgnkx' # sample

disk = [[x for x in range(128)] for _ in range(128)]

def knot_hash(knot,S):
    knot = [x for x in range(256)]
    pos = 0
    skip = 0
    for _ in range(64):
        for l in S:
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
    
    dense_hash = [functools.reduce(lambda x,y:x^y,knot[i:i+16]) for i in range(0,256,16)]
    h = ''
    for d in dense_hash:
        h += "{:02x}".format(d)
    return h 

disk_hash = []
for row in range(len(disk)):
    OS = [ord(x) for x in key+'-'+str(row)]
    OS += [17, 31, 73, 47, 23]
    kh = knot_hash(disk[row],OS)
    b = ''.join(bin(int(h,16))[2:].zfill(4) for h in kh)
    #print(b)
    disk_hash.append(b)
    
#print(disk_hash)
used = 0
print(len(disk_hash))
for row in range(len(disk_hash)):
    used += disk_hash[row].count('1')
    #print(disk_hash[row][0:8].replace('1','#').replace('0','.'))
    #print(disk_hash[row], len(disk_hash[row]))
print("Part 1")
print(used)

seen = collections.defaultdict(int)


surr = [(0,1),(1,0),(0,-1),(-1,0)] # r,c
def in_grid(r,c):
    return 0 <= r < 128 and 0 <= c < 128

def surrounding_groups(row,col):
    g = []
    for s in surr:
        if (row+s[0],col+s[1]) in seen:
            g.append(seen[(row+s[0],col+s[1])])
    print(g)
    return g

def neighbors(row,col):
    N = []
    for s in surr:
        r,c = (row+s[0],col+s[1])
        if not (r,c) in seen and in_grid(r,c) and disk_hash[r][c] == '1':
            N.append((r,c))
    return N
group = 0

def flood_fill(row,col,g):
    valid_neighbors = set(neighbors(row,col))
    while valid_neighbors:
        add_n = set()
        rem_n = set()
        for n in valid_neighbors:
            if n not in seen:
                seen[n] = g
                add_n |= set(neighbors(*n))
            rem_n.add(n)
        valid_neighbors |= add_n
        valid_neighbors -= rem_n

for row in range(len(disk_hash)):
    for col in range(len(disk_hash[row])):
        if disk_hash[row][col] == '1' and (row,col) not in seen:
            seen[(row,col)] = group
            flood_fill(row,col,group)
            group += 1

print(group)
