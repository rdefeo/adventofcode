#!/usr/bin/env python3

### Advent of Code - 2020 - Day 24

import sys
import requests
import re
import math
import itertools
import functools
import os
import collections
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


# Hex tiling algorithms - https://www.redblobgames.com/grids/hexagons/
# For this problem, we're using the odd-r tiling
# Throwback to AoC 2017 Day 11 !!

move_to_odd = {
    'e' : lambda p: (p[0]+1,p[1]),
    'se': lambda p: (p[0]+1,p[1]+1),
    'sw': lambda p: (p[0],p[1]+1),
    'w' : lambda p: (p[0]-1,p[1]),
    'nw': lambda p: (p[0],p[1]-1),
    'ne': lambda p: (p[0]+1,p[1]-1),
}
move_to_even = {
    'e' : lambda p: (p[0]+1,p[1]),
    'se': lambda p: (p[0],p[1]+1),
    'sw': lambda p: (p[0]-1,p[1]+1),
    'w' : lambda p: (p[0]-1,p[1]),
    'nw': lambda p: (p[0]-1,p[1]-1),
    'ne': lambda p: (p[0],p[1]-1),
}

def move_to(d,pos):
    if pos[1]&1: # is y odd?
        return move_to_odd[d](pos)
    else:
        return move_to_even[d](pos)

# Part 1
tiles = collections.defaultdict(int)  # 0 = white, 1 = black
for flips in input_lines:
    i = 0
    pos = (0,0)
    while i < len(flips):
        if flips[i] == 'e' or flips[i] == 'w':
            pos = move_to(flips[i],pos)
        else:
            pos = move_to(flips[i:i+2],pos)
            i += 1
        i += 1
    tiles[pos] = not tiles[pos]

black = sum(tiles.values())
part1(black)


# Part 2

def get_neighbors(pos):
    if pos[1]&1: # is y odd?
        for move in move_to_odd.values():
            yield move(pos)
    else:
        for move in move_to_even.values():
            yield move(pos)

for d in range(100):
    # for every black tile, make sure all of it's
    # neighbors are in (tiles). this let's us possibly
    # flip white tiles that are on the border of our 
    # black tile areas
    black_tiles = [t for t in tiles if tiles[t]]
    for t in black_tiles:
        for n in get_neighbors(t):
            tiles[n] # create a new (white) tile if not present
    
    state = tiles.copy()
    for t in state:
        black = sum(tiles[n] for n in get_neighbors(t))
        # flip'em
        if tiles[t]: # currently black
            if black == 0 or black > 2:
                state[t] = 0
        else:
            if black == 2:
                state[t] = 1
    tiles = state
    #print(f"Day {d+1}:",sum(tiles[t] for t in tiles))

black = sum(tiles.values())
part2(black)