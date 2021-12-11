#!/usr/bin/env python3

### Advent of Code - 2018 - Day 25

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as one long string and as an array of lines
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

class P:
    def __init__(self,pts):
        self.x = pts[0]
        self.y = pts[1]
        self.z = pts[2]
        self.w = pts[3]
    def __repr__(self):
        return str((self.x,self.y,self.z,self.w))
    def mdist(self,s):
        return abs(self.x-s.x)+abs(self.y-s.y)+abs(self.z-s.z)+abs(self.w-s.w)
    
Points = []
for line in input_lines:
    p = P(list(map(int,line.split(','))))
    Points.append(p)

C = []
for p in Points:
    added = False
    for const in C:
        for star in const:
            if p.mdist(star) <= 3:
                added = True
                break
        if added:
            const.append(p)
            break
    if not added:
        C.append([p])
print(len(C)) # First pass

# now we need to check if any constellations can merge!
# Use union/find

def can_merge(c1,c2):
    if not c1 or not c2:
        return False
    for p1 in c1:
        for p2 in c2:
            if p1.mdist(p2) <= 3:
                return True
    return False

while True:
    merged = False

    for i,const1 in enumerate(C):
        for j,const2 in enumerate(C):
            if const1 and const2 and const1 != const2 and can_merge(const1,const2):
                C[j].extend(C[i])
                C[i] = []
                merged = True
    if not merged:
        break
print(C)
print(len(C))

# Paulson:
# C = [set() for _ in range(len(Points))]
# for i,p in enumerate(Points):
#     for j,q in enumerate(Points):
#         if p.mdist(q) <= 3:
#             C[i].add(j)
# S = set()
# ans = 0
# for i in range(len(Points)):
#     if i in S:
#         continue
#     ans += 1
#     Q = [i]
#     while Q:
#         x = Q.pop(0)
#         if x in S:
#             continue
#         S.add(x)
#         for y in C[x]:
#             Q.append(y)
# print(ans)
