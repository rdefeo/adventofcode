#!/usr/bin/env python3

### Advent of Code - 2018 - Day 18

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import copy

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

area = dict()
for y,line in enumerate(input_lines):
    for x,d in enumerate(line):
        area[(y,x)] = d

min_x = min(d[1] for d in area)
min_y = min(d[0] for d in area)
max_x = max(d[1] for d in area)
max_y = max(d[0] for d in area)

def neighbors(p):
    for y in [-1,0,1]:
        for x in [-1,0,1]:
            if y == x == 0:
                continue
            yield (p[0]+y,p[1]+x)

def nacres(area,p):
    acres = collections.defaultdict(int)
    for n in neighbors(p):
        if in_area(n):
            acres[area[n]] += 1
    #print(acres)
    return acres

def in_area(p):
    return min_y <= p[0] <= max_y and min_x <= p[1] <= max_x

def parea(area):
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            print(area[(y,x)],end='')
        print('')
    print('')

# parea(area)

def evolve(area):
    a = copy.deepcopy(area)
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            n = nacres(area,(y,x))
            if area[(y,x)] == '.' and n['|'] >= 3:
                # print("Open turning to Trees")
                a[(y,x)] = '|'
            elif area[(y,x)] == '|' and n['#'] >= 3:
                # print("Trees turning to Lumberyard")
                a[(y,x)] = '#'
            elif area[(y,x)] == '#' and (not n['#'] or not n['|']):
                # print("Lumberyard turning to Open")
                a[(y,x)] = '.'
            else:
                a[(y,x)] = area[(y,x)]
    return a

value = collections.defaultdict(int)
loop = []
for m in range(1000000000):
    # Looks like the pattern starts to loop after a few hundred evolutions
    # so we don't need to do all billion
    if m > 525:
        break
    area = evolve(area.copy())
    # parea(area)
    trees = sum([a=='|' for a in area.values()])
    lumberyards = sum([a=='#' for a in area.values()])
    if m == 9: # Part 1
        print("Evolution:",m+1)
        part1(trees*lumberyards)
    # Keep track of the values we've seen, to detect the loop
    value[(trees,lumberyards)] += 1
    if value[(trees,lumberyards)] == 4:
        # OK, we've seen these values 4 times, clearly, we're looping
        loop.append(trees*lumberyards)

# After watching our printouts, we saw that our 4th loop started at minute 491
# And we noticed that our loop was 28 minutes in length
# Therefore, we can compute our 1B value by looking it up in our recorded loop values
print((1000000000-491)%28)
part2(loop[(1000000000-491)%28])
