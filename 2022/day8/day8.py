#!/usr/bin/env python3

### Advent of Code - 2022 - Day 8

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

heights = collections.defaultdict(int)
H = len(input_lines)
W = len(input_lines[0])

for r in range(len(input_lines)):
    for c in range(len(input_lines[r])):
        heights[(c,r)] = int(input_lines[r][c])
print(W,H)

# Part 1
# for every spot on the grid, check all 4 cardinal directions for strict less than
# if we can see a spot from one of the directions, stop checking
vis = 0
for r in range(H):
    for c in range(W):
        # check outer edges
        if c == 0 or c == W-1 or r == 0 or r == H-1:
            vis += 1
            continue
        # check left
        left = [heights[(ci,r)] for ci in range(c-1,-1,-1)]
        if all(h < heights[(c,r)] for h in left):
            # print(f'left: ({c},{r}) good')
            vis += 1
            continue
        # check up
        up = [heights[(c,ri)] for ri in range(r-1,-1,-1)]
        if all(h < heights[(c,r)] for h in up):
            # print(f'up: ({c},{r}) good')
            vis += 1
            continue
        # check right
        right = [heights[(ci,r)] for ci in range(c+1,W)]
        if all(h < heights[(c,r)] for h in right):
            # print(f'right: ({c},{r}) good')
            vis += 1
            continue
        # check down
        down = [heights[(c,ri)] for ri in range(r+1,H)]
        if all(h < heights[(c,r)] for h in down):
            # print(f'down: ({c},{r}) good')
            vis += 1
            continue

part1(vis)

# Part 2
# for every spot on the grid, check all 4 cardinal directions for greater than or equal to
# but once we find a greater than or equal, count it
scenic = dict()
for r in range(H):
    for c in range(W):
        # check left
        left = 0
        for h in [heights[(ic,r)] for ic in range(c-1,-1,-1)]:
            if h < heights[(c,r)]:
                left += 1
            else:
                if h >= heights[(c,r)]:
                    left += 1
                    break
                break
        # check up
        up = 0
        for h in [heights[(c,ir)] for ir in range(r-1,-1,-1)]:
            if h < heights[(c,r)]:
                up += 1
            else:
                if h >= heights[(c,r)]:
                    up += 1
                    break
                break
        # check right
        right = 0
        for h in [heights[(ic,r)] for ic in range(c+1,W)]:
            if h < heights[(c,r)]:
                right += 1
            else:
                if h >= heights[(c,r)]:
                    right += 1
                    break
                break
        # check down
        down = 0
        for h in [heights[(c,ir)] for ir in range(r+1,H)]:
            if h < heights[(c,r)]:
                down += 1
            else:
                if h >= heights[(c,r)]:
                    down += 1
                    break
                break
        # print(f'{c},{r} = {[up,right,down,left]}',end=' ')
        scene = 1
        for s in [up,right,down,left]:
            scene *= s
        scenic[(c,r)] = scene

part2(max(scenic.values()))







