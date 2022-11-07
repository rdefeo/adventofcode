#!/usr/bin/env python3

### Advent of Code - 2016 - Day 16

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

m = {'0':'1','1':'0'}
def dragon(a):
    b = ''
    for x in reversed(a):
        b += m[x]
    return a+'0'+b

def checksum(a,l):
    s = a[:l]
    while len(s)%2 == 0:
        c = ''
        i = 0
        while i < len(s)-1:
            if s[i] == s[i+1]:
                c += '1'
            else:
                c += '0'
            i += 2
        s = c
    return s

# example data
# ds = 20
# i = '10000'

# Part 1
ds = 272
i = '10001001100000001'

while len(i) < ds:
    i = dragon(i)
part1(checksum(i,ds))

# Part 2
ds = 35651584
while len(i) < ds:
    i = dragon(i)
part2(checksum(i,ds))