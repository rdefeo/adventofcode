#!/usr/bin/env python3

### Advent of Code - 2018 - Day 23

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

# Our Bot - also used as a simple 3D point class when r=0
class Bot:
    def __init__(self,x,y,z,r=0):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
    def __repr__(self):
        return f"{self.x},{self.y},{self.z} : {self.r}"
    def dist(self, b): # distance to another Bot/point
        return abs(self.x-b.x)+abs(self.y-b.y)+abs(self.z-b.z)
    def odist(self): # distance to the origin
        return abs(self.x)+abs(self.y)+abs(self.z)

bots = []
for bot in input_lines:
    m = list(map(int,re.findall(r"-?\d+",bot)))
    bots.append(Bot(*m))

# Part1
# Sort our bots by their radius, then find all bots that are 
# within its range
strongest = sorted(bots,key=lambda b:b.r)[-1]
print(strongest)
inrange = 0
for b in sorted(bots,key=lambda b:b.r):
    if b.dist(strongest) <= strongest.r:
        inrange += 1
part1(inrange)

# Part 2
# Start by creating a cube the size of the entire bot cloud
# Then find all bots that are within the range of the cube
# Once you found the cube that has the most bots in range, shrink
# the cube by half and search within
# Stop once the cube size goes below 1
min_x = min([b.x for b in bots])
max_x = max([b.x for b in bots])
min_y = min([b.y for b in bots])
max_y = max([b.y for b in bots])
min_z = min([b.z for b in bots])
max_z = max([b.z for b in bots])

cubesize = max_x - min_x
best_spot = None
while cubesize > 0:
    max_count = 0
    for x in range(min_x,max_x+1,cubesize):
        for y in range(min_y,max_y+1,cubesize):
            for z in range(min_z,max_z+1,cubesize):
                count = 0
                current_spot = Bot(x,y,z)
                for b in bots:
                    if b.dist(current_spot)-b.r < cubesize:
                        count += 1
                if count > max_count:
                    max_count = count
                    best_spot = current_spot
                elif count == max_count:
                    if not best_spot or current_spot.odist() < best_spot.odist():
                        best_spot = current_spot
    min_x = best_spot.x - cubesize
    max_x = best_spot.x + cubesize
    min_y = best_spot.y - cubesize
    max_y = best_spot.y + cubesize
    min_z = best_spot.z - cubesize
    max_z = best_spot.z + cubesize

    cubesize = cubesize // 2
    
part2(best_spot)
part2(best_spot.odist())

