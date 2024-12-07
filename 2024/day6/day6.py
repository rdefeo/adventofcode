#!/usr/bin/env python3

### Advent of Code - 2024 - Day 6

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

# The '!' let's us know we're out of bounds
grid = collections.defaultdict(lambda : '!')

guard = (0,0)
for r, row in enumerate(input_lines):
    for c, ch in enumerate(row):
        if ch == '^':
            guard = (c,r)
            ch = '.'
        grid[(c,r)] = ch
print(f"{guard=}")

turn_right = {
    (0,-1) : (1,0),
    (1,0) : (0,1),
    (0,1) : (-1,0),
    (-1,0) : (0,-1)
}

# In grid, starting at guard position, find our path
# If we exit the grid, return True and all (positions,directions) visited
# If we get stuck in a loop, return False
def find_path(grid,guard,p2=False):
    visited = []
    turns = set()
    dir = (0,-1) # we always start pointing up
    while True:
        visited.append((guard,dir)) # record our current pos and dir
        np = (guard[0]+dir[0],guard[1]+dir[1]) # get our next pos
        if grid[np] == '#': # if obstacle, turn right
            if p2 and (guard,dir) in turns: # if we've seen this turn before, loop!
                return False, None
            turns.add((guard,dir))
            dir = turn_right[dir]
            continue
        if grid[np] == '!': # out of bounds
            break
        guard = np
    return True, visited

_, visited = find_path(grid, guard)
# print(visited)
part1(len(set([v for v,_ in visited])))

# For ever position we visited, place an obstacle ahead of us and try
# to find a path, counting the loops
loops = 0
seen = set()
for g,d in visited:
    # record where we've been so we don't put an obstacle there, or else
    # we can't be where we are now! (like time traveling to the past and killing your grandfather!)
    seen.add(g)
    np = (g[0]+d[0],g[1]+d[1])
    if grid[np] == '.' and not np in seen:
        grid[np] = '#' # place an obstacle in front of us
        success, _ = find_path(grid, guard, True)
        if not success:
            loops += 1
        grid[np] = '.' # remove obstacle
# print(loops)
part2(loops)