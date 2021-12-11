#!/usr/bin/env python3

### Advent of Code - 2018 - Day 17

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


UP    = (-1,0)
RIGHT = (0,1)
DOWN  = (1,0)
LEFT  = (0,-1)

def padd(a,b):
    return (a[0]+b[0],a[1]+b[1])

def gprint(ground):
    for y in range(min_y,max_y+1):
        for x in range(min_x-1,max_x+2):
            print(ground[(y,x)],end='')
        print('')

ground = collections.defaultdict(lambda:'.')

for line in input_lines:
    m = re.match(r"(\w)=(\d+), (\w)=(\d+)\.\.(\d+)",line)
    if m.group(1) == 'x':
        for y in range(int(m.group(4)),int(m.group(5))+1):
            ground[(y,int(m.group(2)))] = '#'
    if m.group(1) == 'y':
        for x in range(int(m.group(4)),int(m.group(5))+1):
            ground[(int(m.group(2)),x)] = '#'

min_x = min(g[1] for g in ground)-1
max_x = max(g[1] for g in ground)+1
min_y = min(g[0] for g in ground)-1
max_y = max(g[0] for g in ground)+1

spring = (0,500)

# looks left or right (based on d) until we hit a wall or detect
# an overflow. if we overflow, add it to our water sources
# returns how far left/right we went, and whether we overflowed or not
def search(y,x,d,ground,sources):
    while True:
        curr = ground[(y,x)]
        if curr == '#':
            x -= d
            return x, False
        below = ground[(y+1,x)]
        if below == '.':
            sources.append((y,x))
            return x, True
        if curr == '|' and below == '|':
            return x, True
        x += d


ground[spring] = '|'

sources = [spring]
while sources:
    y,x = sources.pop()
    if ground[(y,x)] == '~':
        continue
    
    # for each source, flow down as far as possible
    y += 1
    while y < max_y:
        s = ground[(y,x)]
        if s == '.':
            ground[(y,x)] = '|'
            y += 1
        # if we hit cave or standing water, spread left and right
        elif s in '#~':
            y -= 1
            left,left_overflow = search(y,x,-1,ground,sources)
            right,right_overflow = search(y,x,1,ground,sources)
            overflow = left_overflow or right_overflow
            # flow left/right
            for nx in range(left,right+1):
                ground[(y,nx)] = '|' if overflow else '~'
        elif s == '|':
            break
    # gprint(ground)
gprint(ground)
part1(sum([s in '~|' for p,s in ground.items() if p[0]>min_y]))

part2(sum([s == '~' for p,s in ground.items() if p[0]>min_y]))