#!/usr/bin/env python3

### Advent of Code - 2023 - Day 17

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import heapq

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

grid = dict()
HEIGHT = len(input_lines)
WIDTH = len(input_lines[0])
for y, line in enumerate(input_lines):
    for x, v in enumerate(line):
        grid[(x,y)] = int(v)

NORTH, EAST, SOUTH, WEST = (0,-1), (1,0), (0,1), (-1,0)

def find_path(grid, min_steps, max_steps):
    spos = (0,0) # starting position, with only two possible routes
    epos = (WIDTH-1,HEIGHT-1)

    # (heat loss, position, dir to travel)
    q = [ (0, spos, EAST), (0, spos, SOUTH) ]
    min_hl = collections.defaultdict(lambda: float("inf"))

    while q:
        hl, p, d = heapq.heappop(q)

        if p == epos:
            part1(f"Total heat loss: {hl}")
            return hl

        # have we been at pos 'p', travelling in dir 'd' with a lower heat loss?
        if hl > min_hl[(p,d)]:
            continue
        
        # for dir 'd', we must turn left or right
        for ndir in [(-d[1],d[0]), (d[1],-d[0])]:
            next_hl = hl
            # try walking in ndir up to max_steps. if each iteration is considered
            # "good", add it to our queue
            for steps in range(1,max_steps+1):
                next_p = (p[0] + ndir[0]*steps, p[1] + ndir[1]*steps)
                if next_p not in grid: continue
                
                # for Part 2, we keep accumulating our heat loss (next_hl) until we've
                # gone at least min_steps
                next_hl += grid[next_p]
                if steps < min_steps: continue

                # travelling to next_p is good! add it to queue
                if next_hl < min_hl[(next_p,ndir)]:
                    min_hl[(next_p,ndir)] = next_hl
                    heapq.heappush(q, (next_hl, next_p, ndir))
    return float("inf")

part1(find_path(grid,1,3))
part2(find_path(grid,4,10))