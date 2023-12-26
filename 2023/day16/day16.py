#!/usr/bin/env python3

### Advent of Code - 2023 - Day 16

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

HEIGHT = len(input_lines)
WIDTH = len(input_lines[0])

grid = dict()
for y, line in enumerate(input_lines):
    for x, s in enumerate(line):
        grid[(x,y)] = (s, (False,False,False,False)) # nothing starts "energized", from any dir

NORTH, EAST, SOUTH, WEST = (0,-1), (1,0), (0,1), (-1,0)
ENTERED = { NORTH: 0, EAST: 1, SOUTH: 2, WEST: 3 }

def enter(ent,dir):
    e = list(ent)
    e[ENTERED[dir]] = 1
    return tuple(e)

def move_beam(pos,dir):
    npos = (pos[0]+dir[0],pos[1]+dir[1])
    return (npos,dir)

def energize(grid, starting_pos=(0,0), starting_dir=EAST):
    g = grid.copy()
    beams = []
    beams.append((starting_pos, starting_dir))
    while beams:
        pos, dir = beams.pop(0)
        if pos not in g: continue
        s, energy = g[pos]
        if energy[ENTERED[dir]]: continue
        g[pos] = (s,enter(energy,dir)) # energize!

        if s == '.' or \
           (s == '|' and (dir == NORTH or dir == SOUTH)) or \
           (s == '-' and (dir == EAST or dir == WEST)):
            beams.append(move_beam(pos,dir))
        elif s == '|' and (dir == EAST or dir == WEST):
            beams.append(move_beam(pos,NORTH))
            beams.append(move_beam(pos,SOUTH))
        elif s == '-' and (dir == NORTH or dir == SOUTH):
            beams.append(move_beam(pos,EAST))
            beams.append(move_beam(pos,WEST))
        elif s == '/':
            if dir == EAST:
                beams.append(move_beam(pos,NORTH))                
            elif dir == NORTH:
                beams.append(move_beam(pos,EAST))                
            elif dir == WEST:
                beams.append(move_beam(pos,SOUTH))                
            else:
                beams.append(move_beam(pos,WEST))
        elif s == '\\':
            if dir == EAST:
                beams.append(move_beam(pos,SOUTH))                
            elif dir == NORTH:
                beams.append(move_beam(pos,WEST))
            elif dir == WEST:
                beams.append(move_beam(pos,NORTH))                
            else:
                beams.append(move_beam(pos,EAST))
    return g

def get_energized(grid):
    return sum(sum(grid[(x,y)][1]) > 0 for x in range(WIDTH) for y in range(HEIGHT))

part1(get_energized(energize(grid)))

# let's try every starting position and find the max
max_energy = 0
for x in range(0,WIDTH):
    max_energy = max(max_energy, get_energized(energize(grid,(x,0),SOUTH)))
    max_energy = max(max_energy, get_energized(energize(grid,(x,HEIGHT-1),NORTH)))
for y in range(0,HEIGHT):
    max_energy = max(max_energy, get_energized(energize(grid,(0,y),EAST)))
    max_energy = max(max_energy, get_energized(energize(grid,(WIDTH-1,y),WEST)))
part2(max_energy)
