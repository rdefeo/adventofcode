#!/usr/bin/env python3

### Advent of Code - 2022 - Day 14

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

CAVE = collections.defaultdict(lambda : '.')
left = top = 9999999
right = bottom = -9999999
SO = [500,0]
CAVE[tuple(SO)] = '+'  # sand origin

# build the rock segments
def create_rock(x1,y1,x2,y2):
    global CAVE
    global left, right, top, bottom
    if x1 == x2:
        yo = sorted([y1,y2])
        for y in range(yo[0],yo[1]+1):
            CAVE[(x1,y)] = '#'
    elif y1 == y2:
        xo = sorted([x1,x2])
        for x in range(xo[0],xo[1]+1):
            CAVE[(x,y1)] = '#'
    left = min(left,x1,x2)
    right = max(right,x1,x2)
    top = min(top,y1,y2)
    bottom = max(bottom,y1,y2)

# parse the rock cave input
for rocks in input_lines:
    points = re.findall(r'(\d+),(\d+)',rocks)
    for a,b in zip(points,points[1:]):
        create_rock(int(a[0]),int(a[1]),int(b[0]),int(b[1]))

def print_rocks(cave):
    for y in range(0, bottom + 2):
        for x in range(left-1,right+1):
            print(cave[(x,y)],end='')
        print()
    print()

# our starting cave
print_rocks(CAVE)

def drop_sand(cave):
    s = SO.copy()
    while s[1] < bottom:
        if cave[(s[0],s[1]+1)] == '.':
            s[1] += 1
            continue
        if cave[(s[0]-1,s[1]+1)] == '.':
            s[0] -= 1
            s[1] += 1
            continue
        if cave[(s[0]+1,s[1]+1)] == '.':
            s[0] += 1
            s[1] += 1
            continue
        break
    return s, cave

def simulate_sand(cave):
    cave = CAVE.copy()
    while(True):
        sand, cave = drop_sand(cave)
        if sand[1] >= bottom:
            break
        cave[tuple(sand)] = 'o'
        if sand == SO: # The sand reached our starting point! Stop!
            break
    return cave

# Part 1
cave = simulate_sand(CAVE)
print_rocks(cave)
part1(sum([1 for y in range(0,bottom+1) for x in range(left-1,right+2) if cave[(x,y)] == 'o']))

# Part 2
# create the "infinite" floor. we can't go wider than our height, but pad it by 2
# I tested this with increasing width and the total sand didn't change, so we're good
create_rock(SO[0]-bottom-2,bottom+2,SO[0]+bottom+2,bottom+2)
cave = simulate_sand(CAVE)
# print_rocks(cave)
part2(sum([1 for y in range(0,bottom+1) for x in range(left-1,right+2) if cave[(x,y)] == 'o']))
