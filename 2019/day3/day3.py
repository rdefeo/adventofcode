#!/usr/bin/env python3

### Advent of Code - 2019 - Day 3

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

def parse_wire(wire):
    ''' "Walk" along the wire, storing the dist at each (x,y) '''
    x, y = 0, 0
    dist = 0
    w = dict()
    for d in wire.split(','):
        dx, dy = {'U':(0,-1),'R':(1,0),'D':(0,1),'L':(-1,0)}[d[0]]
        for _ in range(int(d[1:])):
            x += dx
            y += dy
            dist += 1
            w[(x,y)] = dist
    return w

wire1 = parse_wire(input_lines[0])
wire2 = parse_wire(input_lines[1])

# Determine where the wires share the same (x,y)
intersections = set(wire1.keys()) & set(wire2.keys())

# Part 1
# Manhattan distance of the closest intersection
part1(min([abs(x)+abs(y) for x,y in intersections]))

# Part 2
# Minimum distance along each wire to an intersection
part2(min([wire1[i]+wire2[i] for i in intersections]))
