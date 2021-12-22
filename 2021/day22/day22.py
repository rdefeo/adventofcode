#!/usr/bin/env python3

### Advent of Code - 2021 - Day 22

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

# Part 1
# Simply keep track of every cube since the problem space is small-ish
cubes = set()
for line in input_lines:
    nums = list(map(int,re.findall(r'-?\d+',line)))
    tok = line.split()
    if any(abs(n)>50 for n in nums): continue
    for x in range(nums[0],nums[1]+1):
        for y in range(nums[2],nums[3]+1):
            for z in range(nums[4],nums[5]+1):
                if tok[0] == 'on':
                    cubes.add((x,y,z))
                else:
                    cubes.discard((x,y,z))
part1(len(cubes))


# Part 2
# The solution above won't work for the larger problem space. Instead, keep
# track of each cube bounds in a list. As we parse each new reboot instruction,
# check if this new cube overlaps with any previous cubes. If it does, preserve
# all parts of the previous cube that aren't part of the new cube. Do this by
# breaking it up into pieces and adding those back to our list. Then, if our new
# cube is 'on', add it to the list. If 'off', the space occupied by both cubes
# wouldn't have been preserved by the previous step, therefore, it's no longer
# in the list - 'off'

def cube_size(cube):
    return abs(cube[1]-cube[0]+1)*abs(cube[3]-cube[2]+1)*abs(cube[5]-cube[4]+1)

def cubes_overlap(old,new):
    x_lap = new[1] >= old[0] and new[0] <= old[1]
    y_lap = new[3] >= old[2] and new[2] <= old[3]
    z_lap = new[5] >= old[4] and new[4] <= old[5]
    return x_lap and y_lap and z_lap

cubes = []
for line in input_lines:
    cube = list(map(int,re.findall(r'-?\d+',line)))
    x1,x2,y1,y2,z1,z2 = cube
    tok = line.split()
    new_cubes = []
    for c in cubes:
        if cubes_overlap(c,cube):
            # Split up the existing cube (c) into new cubes, by slicing off parts.
            # e.g. If cube c extends left of the new cube, create a new cube that's
            # everything to the left of the new cube but within c. 2D example:
            #   existing ->     c[0]..............c[1]          
            #   new cube ->                x1...........x2
            #   slice    ->     c[0]....x-1
            # All other bounds (y and z) remain the same. After creating the new
            # cube, reset c[0] to x1, as we just sliced off the left side.
            # Repeat the process for the other 6 sides to end up with all parts
            # of 'c' that are not our new cube. Essentially, we have removed the
            # overlapping region of c and cube from c.
            if c[0] < x1: # left slice
                new_cubes.append([c[0],x1-1,c[2],c[3],c[4],c[5]])
                c[0] = x1
            if c[1] > x2: # right slice
                new_cubes.append([x2+1,c[1],c[2],c[3],c[4],c[5]])
                c[1] = x2
            if c[2] < y1: # bottom slice
                new_cubes.append([c[0],c[1],c[2],y1-1,c[4],c[5]])
                c[2] = y1
            if c[3] > y2: # top slice
                new_cubes.append([c[0],c[1],y2+1,c[3],c[4],c[5]])
                c[3] = y2
            if c[4] < z1: # front slice
                new_cubes.append([c[0],c[1],c[2],c[3],c[4],z1-1])
                c[4] = z1
            if c[5] > z2: # back slice
                new_cubes.append([c[0],c[1],c[2],c[3],z2+1,c[5]])
                # c[5] = z2
        else:
            # our new cube doesn't overlap this existing, add it back to the list
            new_cubes.append(c)
    if tok[0] == 'on':
        # now that all other cubes have been sliced, and any overlapping portions
        # have been removed, let's turn our cube on
        new_cubes.append(cube)
    cubes = new_cubes
part2(sum(map(cube_size,cubes)))

