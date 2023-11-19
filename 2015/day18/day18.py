#!/usr/bin/env python3

### Advent of Code - 2015 - Day 18

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
#input_nums = list(map(int,input_lines))

grid = collections.defaultdict(lambda : '.')

SIZE = len(input_lines)
for r, line in enumerate(input_lines):
    for c, light in enumerate(line):
        grid[(c,r)] = light

# Maintain separate grids for Parts 1 and 2
grid1 = grid.copy()
grid2 = grid.copy()

def count_surrounding_lights(g, c, r):
    """ Return number of ON lights in surrounding cells """
    return sum(g[(c+dc,r+dr)] == '#' for dc, dr in [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)])

def get_next_light_state(curr, on_count):
    """ Apply the game rules based on current state and number of surrounding ON lights """
    if curr == '#' and on_count not in [2, 3]:
        return '.'
    elif curr == '.' and on_count == 3:
        return '#'
    return curr

def count_on_lights(g):
    """ Returns total number of lights ON in the grid """
    return sum(g[(c,r)] == '#' for c in range(SIZE) for r in range(SIZE))

# Iterate each grid to get next state
for _ in range(100):
    g1 = collections.defaultdict(lambda: '.')
    g2 = collections.defaultdict(lambda: '.')

    # Ensure that the corners are always lit for the Part 2 grid
    grid2[(0,0)] = grid2[(0,SIZE-1)] = grid2[(SIZE-1,SIZE-1)] = grid2[(SIZE-1,0)] = '#'

    for r in range(SIZE):
        for c in range(SIZE):
            lon1 = count_surrounding_lights(grid1, c, r)
            g1[(c,r)] = get_next_light_state(grid1[(c,r)], lon1)

            lon2 = count_surrounding_lights(grid2, c, r)
            g2[(c,r)] = get_next_light_state(grid2[(c,r)], lon2)

    grid1 = g1.copy()
    grid2 = g2.copy()

part1(count_on_lights(grid1))

# Our last iteration could have turned OFF corners, force them back ON before counting
grid2[(0,0)] = grid2[(0,SIZE-1)] = grid2[(SIZE-1,SIZE-1)] = grid2[(SIZE-1,0)] = '#'
part2(count_on_lights(grid2))

