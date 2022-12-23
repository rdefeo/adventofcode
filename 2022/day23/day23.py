#!/usr/bin/env python3

### Advent of Code - 2022 - Day 23

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

# Read the grid of elves
grid = collections.defaultdict(lambda:'.')
for y,line in enumerate(input_lines):
    for x,c in enumerate(line):
        grid[(x,y)] = c

# Helper method for printing and iterating grid
def get_min_max(g):
    x = [x for x,y in g]
    y = [y for x,y in g]
    return min(x), max(x), min(y), max(y)

def print_grid(g):
    min_x, max_x, min_y, max_y = get_min_max(g)
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            print(g[(x,y)],end='')
        print()
    print()

# The 3 deltas in each cardinal direction. The [1] element is the true direction
NORTH = [(-1,-1), (0,-1), (1,-1)]
EAST = [(1,-1), (1,0), (1,1)]
SOUTH = [(-1,1), (0,1), (1,1)]
WEST = [(-1,1), (-1,0), (-1,-1)]

# Check each cardinal direction possibilities, rotating the order we look based
# on the current round. The first direction that's clear, assign it to be our move
# If all of the directions are clear, then we don't move
def propose_move(p, g, r):
    dir_clear = [True] * 4
    first_move = (0,0) # or, no move
    for rm in range(r,r+4):
        dir = [NORTH, SOUTH, WEST, EAST][rm%4]
        for d in dir:
            np = (p[0]+d[0],p[1]+d[1])
            if np in g and g[np] == '#':
                dir_clear[rm%4] = False
        if dir_clear[rm%4] and first_move == (0,0):
            first_move = dir[1]
    if all(d for d in dir_clear):
        return (0,0)
    return first_move

r = 0
while True:
    # Go through the grid and determine the proposed move for each elf. Store this
    # as a dict[ (location moving to) ] = [ list of elves who want to move there ]
    # If the value for every key in that dict is 1 element long, then the elf can move.
    proposed = collections.defaultdict(list)
    min_x, max_x, min_y, max_y = get_min_max(grid)

    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            if (x,y) in grid and grid[(x,y)] == '#':
                d = propose_move((x,y),grid,r)
                proposed[(x+d[0],y+d[1])] += [(x,y)]

    new_grid = collections.defaultdict(lambda:'.')
    moved_elves = False
    for p,l in proposed.items():
        if len(l) == 1:
            new_grid[p] = '#'
            if p != l[0]: # check if at least 1 elf is moving
                moved_elves = True
        else:
            for sp in l:
                new_grid[sp] = '#'
    grid = new_grid.copy()
    r += 1

    # Part 1
    if r == 10:
        min_x, max_x, min_y, max_y = get_min_max(grid)
        part1(sum([grid[(x,y)]=='.' for x in range(min_x,max_x+1) for y in range(min_y,max_y+1)]))

    # Part 2
    if not moved_elves:
        part2(r)
        break

# print_grid(grid)