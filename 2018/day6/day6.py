#!/usr/bin/env python3

### Advent of Code - 2018 - Day 6

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

grid = collections.defaultdict(lambda:' ')
coords = collections.defaultdict(int)
for i,coord in enumerate(input_lines):
    x,y = int(coord.split(', ')[0]), int(coord.split(', ')[1])
    grid[(x,y)] = 'X'
    coords[(x,y)] = i
CW = len(str(len(coords)))+1 # text width of our coord id, for printing

# bounds of our grid containing all coords
# don't need to look outside this box
min_x = min(i[0] for i in grid.keys())
max_y = max(i[1] for i in grid.keys())
min_y = min(i[1] for i in grid.keys())
max_x = max(i[0] for i in grid.keys())

def print_grid(grid):
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            print(str(grid[(x,y)]).center(CW),end='')
        print('')

# generator for all coord distances
def coords_dist(x,y):
    for i,c in enumerate(coords):
        dist = abs(x-c[0])+abs(y-c[1])
        yield dist, i

# Part 1
def find_closest(x,y):
    closest = sorted([(dist,coord) for dist,coord in coords_dist(x,y)])
    if closest[0][0] == closest[1][0]:
        return '.'
    else:
        return closest[0][1]

for y in range(min_y,max_y+1):
    for x in range(min_x,max_x+1):
        closest = find_closest(x,y)
        grid[(x,y)] = closest

# print_grid(grid)

# remove any coords found on edges, then count areas of remaining
middle_c = set(list(range(len(coords))))
for c in coords:
    for x in range(min_x,max_x+1):
        middle_c.discard(grid[(x,min_y)])
        middle_c.discard(grid[(x,max_y)])
    for y in range(min_y,max_y+1):
        middle_c.discard(grid[(min_x,y)])
        middle_c.discard(grid[(max_x,y)])

areas = []
for m in middle_c:
    s = sum(v==m for v in grid.values())
    #print(m,s)
    areas.append(s)

part1(f"Largest area: {max(areas)}")

# Part 2
safe_zone = 0
saftey_distance = 32 if len(coords) < 10 else 10000
for y in range(min_y,max_y+1):
    for x in range(min_x,max_x+1):
        if sum([d for d,_ in coords_dist(x,y)]) < saftey_distance:
            safe_zone += 1
part2(f"Safe Zone size: {safe_zone}")