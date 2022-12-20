#!/usr/bin/env python3

### Advent of Code - 2022 - Day 18

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

droplets = set()
for line in input_lines:
    x,y,z = list(map(int,line.split(',')))
    droplets.add((x,y,z))
# print(droplets)

min_x = min(x for x,_,_ in droplets)
min_y = min(y for _,y,_ in droplets)
min_z = min(z for _,_,z in droplets)
max_x = max(x for x,_,_ in droplets)
max_y = max(y for _,y,_ in droplets)
max_z = max(z for _,_,z in droplets)

print(min_x,min_y,min_z)
print(max_x,max_y,max_z)

# Part 1
def find_surface_area(locations):
    areas = collections.defaultdict(int)
    for z in range(min_z,max_z+1):
        for y in range(min_y,max_y+1):
            for x in range(min_x,max_x+1):
                if (x,y,z) in locations:
                    for dx,dy,dz in [(1,0,0),(0,1,0),(-1,0,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                        if (x+dx,y+dy,z+dz) not in locations:
                            areas[(x,y,z)] += 1
    return sum(a for a in areas.values()) 
p1_area = find_surface_area(droplets) 
part1(p1_area)

# Part 2
# for every drop that's not lava, perform a bfs to fill the void, or something
# if we hit an "edge", it's not in a void! keep track of locations that are void/non-void
voids = dict()
for z in range(min_z,max_z+1):
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            visited = set() # all locations we've seen during this "bloom"
            if (x,y,z) not in droplets:
                q = [(x,y,z)]
                while q:
                    (vx,vy,vz) = q.pop(0)
                    if (vx,vy,vz) in droplets: continue
                    # did we hit an edge?
                    if vx <= min_x or vy <= min_y or vz <= min_z or vx >= max_x or vy >= max_y or vz >= max_z:
                        # add ourselves and all visited locations as non-void
                        for v in visited: # is this needed?
                            voids[v] = False
                        voids[(x,y,z)] = False
                        break
                    if (vx,vy,vz) in visited: continue
                    visited.add((vx,vy,vz))
                    adj = [(vx+dx,vy+dy,vz+dz) for dx,dy,dz in [(1,0,0),(0,1,0),(-1,0,0),(0,-1,0),(0,0,1),(0,0,-1)]]
                    for n in adj:
                        q.append(n)
                if (x,y,z) not in voids:
                    voids[(x,y,z)] = True
print(f"num droplets: {len(droplets)}")
voids = set(v for v in voids if voids[v] == True)
print(f"num voids: {len(voids)}")
p2_area = find_surface_area(voids)
print(p2_area)
part2(p1_area-p2_area)