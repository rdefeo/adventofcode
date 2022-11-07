#!/usr/bin/env python3

### Advent of Code - 2016 - Day 24

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
from heapq import heappop, heappush

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



ducts = {}
numbers = []
origin = None
for i,y in enumerate(input_lines):
    for j,x in enumerate(y):
        if x == '0':
            origin = (j,i)
        elif x.isdigit():
            numbers.append((j,i))
        ducts[(j,i)] = x

max_y = len(input_lines)
max_x = len(input_lines[0])
def print_ducts(ducts):
    for y in range(max_y):
        for x in range(max_x):
            print(ducts[(x,y)],end='')
        print('')

print_ducts(ducts)
print(numbers)

def neighbors(x,y):
    directions = [(1,0),(0,1),(-1,0),(0,-1)] # R,D,L,U
    return [(x+d[0],y+d[1]) for d in directions]

def is_wall(x,y):
    return ducts[(x,y)] == '#'
print(origin)

# BFS from point a to point b
def visit_a_to_b(a,b):
    heap = [(0,a)] # dist,(x,y)
    visited = { a:0 } # pos: dist
    while heap:
        dist,(x,y) = heappop(heap)
        if (x,y) == b:
            return dist
        dist += 1
        for nx,ny in neighbors(x,y):
            if is_wall(nx,ny) or (nx,ny) in visited:
                continue
            visited[(nx,ny)] = dist
            heappush(heap,(dist,(nx,ny)))

# compute min distance from starting point to all other points
dist_from_0 = [visit_a_to_b(origin,b) for b in numbers]
N = len(numbers)
dists = [[None for j in range(N)] for i in range(N)]

# compute the min distance from each point to each other
for i in range(N):
    for j in range(i+1,N):
        dists[j][i] = dists[i][j] = visit_a_to_b(numbers[i],numbers[j])

# starting with point '0', calculate the total distance for every
# permutation of paths to each point
# for part 2, add the distance from the last point back to the origin
part_1 = part_2 = 99999999999
for path in itertools.permutations(range(N)):
    d = dist_from_0[path[0]]
    for i in range(len(path)-1):
        d += dists[path[i]][path[i+1]]
    part_1 = min(part_1,d)
    # part 2
    d += dist_from_0[path[-1]]
    part_2 = min(part_2,d)
part1(part_1)
part2(part_2)

