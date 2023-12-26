#!/usr/bin/env python3

### Advent of Code - 2023 - Day 18

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

p1_dirs, p1_dists = [], []
p2_dirs, p2_dists = [], []

for line in input_lines:
    dir, dist, color = line.split()    
    p1_dirs.append(dir)
    p1_dists.append(int(dist))

    # split color into dist/dir
    color = color[1:-1]
    p2_dists.append(int(color[1:-1],16))
    p2_dirs.append('RDLU'[int(color[-1])])

def gen_vertices(dirs, dists):
    """ Returns the list of vertices and total path length. The
    input was verified that we always form a closed loop and
    return to the first vertex. """
    x, y, plen = 0, 0, 0
    vertices = []
    for dir, dist in zip(dirs,dists):
        plen += dist
        if dir == 'U':
            y -= dist
        elif dir == 'R':
            x += dist
        elif dir == 'D':
            y += dist
        else:
            x -= dist
        vertices.append((x,y))
    return vertices, plen

def shoelace_area(verts):
    """ Shoelace Formula:
    Cross-multiply the coordinates for every pair of vertices 
    and accumulate their differences. """
    s = 0
    for a,b in zip(verts,verts[1:]+[verts[0]]):
        s += a[0]*b[1] - a[1]*b[0]
    return abs(s) // 2

vertices, plen = gen_vertices(p1_dirs,p1_dists)
part1(shoelace_area(vertices)+plen//2+1) # account for path length

vertices, plen = gen_vertices(p2_dirs,p2_dists)
part2(shoelace_area(vertices)+plen//2+1)