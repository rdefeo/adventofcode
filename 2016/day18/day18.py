#!/usr/bin/env python3

### Advent of Code - 2016 - Day 18

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



# tiles = '.^^.^.^^^^' # test

def next_tiles(tiles):
    nt = ''
    i = 0
    while i < len(tiles):
        l = r = 'x'
        if i == 0:
            l = '.'
        else:
            l = tiles[i-1]
        if i == len(tiles)-1:
            r = '.'
        else:
            r = tiles[i+1]
        c = tiles[i]
        if l == c == '^' and r == '.':
            nt += '^'
        elif l == '.' and c == r == '^':
            nt += '^'
        elif l == '^' and c == r == '.':
            nt += '^'
        elif l == c == '.' and r == '^':
            nt += '^'
        else:
            nt += '.'
        i += 1
    return nt

# part 1
tiles = input.strip()
safe = tiles.count('.')
for _ in range(40-1):
    tiles = next_tiles(tiles)
    safe += tiles.count('.')
# print('\n'.join(floor))
part1(safe)

# part 2
tiles = input.strip()
safe = tiles.count('.')
for _ in range(400000-1):
    tiles = next_tiles(tiles)
    safe += tiles.count('.')
# print('\n'.join(floor))
part2(safe)