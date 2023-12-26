#!/usr/bin/env python3

### Advent of Code - 2023 - Day 22

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

bricks = []
for id, line in enumerate(input_lines):
    c1, c2 = line.split('~')
    c1 = tuple(map(int,c1.split(',')))
    c2 = tuple(map(int,c2.split(',')))
    # this means c1 is always the lower corner (in each dim)
    assert c1[0] <= c2[0]
    assert c1[1] <= c2[1]
    assert c1[2] <= c2[2]
    bricks.append((c1,c2))
bricks.sort(key=lambda x: x[0][2]) # This is essential for dropping correctly

# Let's make our list of bricks "fall". Since we sorted our bricks
# by z-order, everything will fall correctly
def drop_bricks(bricks):
    """ Knowing that our blocks are sorted by z value, we build a height map starting
    at the floor. Each block is then pushed down to the max value in the height map
    that covers the base of our brick. We keep track of how many bricks actually
    moved down. """
    stack = []
    height = collections.defaultdict(int) # height off the floor
    drop_count = 0
    for (c1,c2) in bricks:
        # find the max height under our brick base (x by y)
        mh = 0
        for x in range(c1[0],c2[0]+1):
            for y in range(c1[1],c2[1]+1):
                mh = max(mh,height[(x,y)])
        # we can now drop our brick down to mh+1
        if mh+1 < c1[2]:
            drop = c1[2] - (mh+1)
            c1 = (c1[0],c1[1],c1[2]-drop)
            c2 = (c2[0],c2[1],c2[2]-drop)
            drop_count += 1
        # update height map to be the top of our brick
        for x in range(c1[0],c2[0]+1):
            for y in range(c1[1],c2[1]+1):
                height[(x,y)] = c2[2]
        stack.append((c1,c2))
    return stack, drop_count

# Dropping bricks for the first time
bricks, _ = drop_bricks(bricks)

# Parts 1 and 2
# Given our brick stack, try removing each brick and then dropping all of them
# again. If we get back drop_count > 0 then it wasn't safe to remove that brick!
# With this value, Part 2 is simply their sum.
total_not_safe = 0
total_drops = 0
for i in range(len(bricks)):
    new_bricks = bricks[:i] + bricks[i+1:]
    _, drop_count = drop_bricks(new_bricks)
    total_not_safe += drop_count > 0
    total_drops += drop_count
part1(len(bricks) - total_not_safe)
part2(total_drops)
