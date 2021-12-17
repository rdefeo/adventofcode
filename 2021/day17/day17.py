#!/usr/bin/env python3

### Advent of Code - 2021 - Day 17

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as one long string and as an array of lines
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
finput = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in finput.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

n = list(map(int,re.findall(r"-?\d+",finput)))
print(n)
X = (n[0],n[1])
Y = (n[2],n[3])

def step(p,v):
    p = (p[0]+v[0],p[1]+v[1])
    # if we ever have neg x vel, we'll never hit target
    # so only care about the pos and zero cases
    nvx = max(0,v[0]-1)
    return p,(nvx,v[1]-1)

# try different velocities
def solve():
    max_y = 0
    vels = set()
    for vx in range(1,X[1]+1): # never start w/ neg or 0 X vel
        for vy in range(Y[0],abs(Y[0])):
            v = (vx,vy)
            (x,y), my = (0,0), 0
            # print(f"checking {v=}")
            while x < X[1] and y > Y[0]:
                my = max(my,y)
                (x,y), v = step((x,y),v)
                # print(f"  {(x,y)=}, {v=}")
                if X[0] <= x <= X[1] and Y[0] <= y <= Y[1]:
                    print(f"HIT! {(x,y)=}, {(vx,vy)=}")
                    max_y = max(max_y,my)
                    vels.add((vx,vy))
    return max_y,vels

print(f"{X=}")
print(f"{Y=}")
max_y,vels = solve()
# print(vels)
part1(max_y)
part2(len(vels))
            



