#!/usr/bin/env python3

### Advent of Code - 2021 - Day 18

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

# for any pair that's 4 levels deep:
#  - add it's left num to the first num on it's left (if any)
#  - add it's right num to the first num on it's right (if any)
def explode(a):
    depth = 0
    for i,c in enumerate(a):
        if c == '[':
            depth += 1
            if depth == 5:
                x,y = int(a[i+1]),int(a[i+3]) # extract number pair
                left = a[:i] # everything left of pair
                for li in range(len(left)-1,-1,-1):
                    if left[li].isdigit():
                        left[li] = str(int(left[li]) + x) # add to left
                        break
                right = a[i+5:] # everything right of pair
                for ri in range(len(right)):
                    if right[ri].isdigit():
                        right[ri] = str(int(right[ri]) + y) # add to right
                        break
                return left+['0']+right # number pair replaced by 0
        elif c == ']':
            depth -= 1
    return None

# only split the FIRST num > 9 
def split(a):
    for i,c in enumerate(a):
        if c.isdigit() and int(c) > 9:
            return a[:i] + ['[',str(int(c)//2),',',str((int(c)+1)//2),']'] + a[i+1:]
    return None

# compute the magnitude for all pairs
def mag(a):
    if type(a) is list:
        return 3*mag(a[0]) + 2*mag(a[1])
    else:
        return int(a)

# keep trying to explode then split each number
def reduce(a):
    while True:
        res = explode(a)
        if res is not None:
            a = res
            continue
        res = split(a)
        if res is not None:
            a = res
            continue
        return a

# Part 1 - magnitude of the sum of all lines
n = list(input_lines[0])
for i in [list(x) for x in input_lines[1:]]:
    n = reduce(['[']+n+[',']+i+[']'])
part1(mag(eval(''.join(n))))

# Part 2 - max magnitude for the sum of any 2 pair of lines
mags = 0
for i,j in itertools.permutations(range(len(input_lines)),2):
    a = reduce(list(input_lines[i]))
    b = reduce(list(input_lines[j]))
    mags = max(mags,mag(eval(''.join(reduce(['[']+a+[',']+b+[']'])))))
part2(mags)
