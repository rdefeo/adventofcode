#!/usr/bin/env python3

### Advent of Code - 2023 - Day 14

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

grid = dict()
for y, line in enumerate(input_lines):
    for x, r in enumerate(line):
        grid[(x,y)] = r
HEIGHT, WIDTH = len(input_lines), len(input_lines[0])
print(f"{WIDTH=}, {HEIGHT=}")
def pgrid(grid):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print(grid[(x,y)],end='')
        print()
    print()

NORTH, EAST, SOUTH, WEST = (0,-1), (1,0), (0,1), (-1,0)
def tilt(grid, dir):
    ngrid = grid.copy()
    if dir == NORTH:
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if ngrid[(x,y)] == 'O':
                    for ry in range(y,-1,-1):
                        if (x,ry-1) in grid and ngrid[(x,ry-1)] == '.':
                            ngrid[(x,ry)] = '.'
                        else:
                            ngrid[(x,ry)] = 'O'
                            break
    elif dir == EAST:
        for y in range(HEIGHT):
            for x in range(WIDTH-1,-1,-1):
                if ngrid[(x,y)] == 'O':
                    for rx in range(x,WIDTH):
                        if (rx+1,y) in grid and ngrid[(rx+1,y)] == '.':
                            ngrid[(rx,y)] = '.'
                        else:
                            ngrid[(rx,y)] = 'O'
                            break
    elif dir == SOUTH:
        for x in range(WIDTH):
            for y in range(HEIGHT-1,-1,-1):
                if ngrid[(x,y)] == 'O':
                    for ry in range(y,HEIGHT):
                        if (x,ry+1) in grid and ngrid[(x,ry+1)] == '.':
                            ngrid[(x,ry)] = '.'
                        else:
                            ngrid[(x,ry)] = 'O'
                            break
    elif dir == WEST:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if ngrid[(x,y)] == 'O':
                    for rx in range(x,-1,-1):
                        if (rx-1,y) in grid and ngrid[(rx-1,y)] == '.':
                            ngrid[(rx,y)] = '.'
                        else:
                            ngrid[(rx,y)] = 'O'
                            break
    return ngrid

def get_load(grid):
    load = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[(x,y)] == 'O':
                load += HEIGHT-y
    return load

# pgrid(grid)
# pgrid(tilt(grid,NORTH))

part1(get_load(tilt(grid,NORTH)))

def cycle(grid):
    grid = tilt(grid,NORTH)
    grid = tilt(grid,WEST)
    grid = tilt(grid,SOUTH)
    grid = tilt(grid,EAST)
    return grid

def get_rock_state(grid):
    state = set()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[(x,y)] == 'O':
                state.add((x,y))
    return tuple(sorted(state))

CYCLES = 1000000000
rstate = dict()
for c in range(CYCLES):
    state = get_rock_state(grid)
    if state in rstate:
        last_c = rstate[state]
        print(f"Loop found on cycle {c=}, first found on {last_c=}")
        # determine how many times we'll go through this loop before we hit CYCLES
        llen = c - last_c
        print(f"Loop length = {llen}")
        lremain = (CYCLES-last_c) % llen
        print(f"Based on this, we need {lremain=} more cycles")
        for _ in range(lremain):
            grid = cycle(grid)
        part2(get_load(grid))
        break
    grid = cycle(grid)
    rstate[state] = c # save our state and current cycle
