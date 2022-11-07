#!/usr/bin/env python3

### Advent of Code - 2016 - Day 21

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

# positive s is rotate right, negative is left
def rotate(p,s):
    return p[-s:]+p[:-s]

password = list('abcde')
password = list('abcdefgh')
def scramble(p):
    for i in input_lines:
        t = i.split(' ')
        # print(t)
        if i.startswith("swap position"):
            x,y = int(t[2]),int(t[5])
            tmp = p[x]
            p[x] = p[y]
            p[y] = tmp
        elif i.startswith("swap letter"):
            x = p.index(t[2])
            y = p.index(t[5])
            tmp = p[x]
            p[x] = p[y]
            p[y] = tmp
        elif i.startswith("rotate"):
            if t[1] == "left" or t[1] == "right":
                s = int(t[2])
                s = -s if t[1] == "left" else s
                p = rotate(p,s)
            else:
                x = p.index(t[6])
                p = rotate(p,1)
                p = rotate(p,x)
                if x >= 4:
                    p = rotate(p,1)
        elif i.startswith("reverse"):
            x,y = int(t[2]),int(t[4])
            head, tail = [], []
            if x > 0:
                head = p[:x]
            if y < len(p)-1:
                tail = p[y+1:]
            p = head + list(reversed(p[x:y+1])) + tail
        elif i.startswith("move"):
            x,y = int(t[2]),int(t[5])
            m = p[x]
            p.remove(m)
            p.insert(y,m)
    return ''.join(p)
part1(scramble(password))

# Part 2 - reverse the scramble steps. but, just compute all
# permutations until we find the requested input

unscrambled = 'fbgdceah'
for p in itertools.permutations('abcdefgh'):
    if scramble(list(p)) == unscrambled:
        part2(''.join(p))
        break

