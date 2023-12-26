#!/usr/bin/env python3

### Advent of Code - 2023 - Day 21

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

grid = dict()
spos = (0,0)
WIDTH, HEIGHT = len(input_lines[0]), len(input_lines)
assert WIDTH == HEIGHT
SIZE = WIDTH

for y, line in enumerate(input_lines):
    for x, p in enumerate(line):
        if p == 'S':
            spos = (x,y)
            grid[(x,y)] = '.'
        else:
            grid[(x,y)] = p

NORTH, EAST, SOUTH, WEST = (0,-1), (1,0), (0,1), (-1,0)

def pgrid(pset):
    """ Prints the grid, showing the location of where you've walked to """
    for y in range(SIZE):
        for x in range(SIZE):
            if (x,y) in pset:
                print('O',end='')
            else:
                print(grid[(x,y)],end='')
        print()
    print()

# Part 1
# Straight forward BFS which walks 'n' steps from 'spos'
def walk_steps(n, spos):
    q = [ (n, spos) ] # step remaining, position
    plots = set()
    visited = set()
    while q:
        steps, pos = q.pop(0)

        # If we have an even number of steps remaining, then we will always have a
        # path back to this position. For example: 1 step north, 1 step south, repeat...
        # Therefore, add it to our list.
        if steps %2 == 0:
            plots.add(pos)

        if steps == 0:
            plots.add(pos)
            continue

        for dx,dy in [NORTH, EAST, SOUTH, WEST]:
            npos = (pos[0]+dx,pos[1]+dy)
            if npos in grid and grid[npos] != '#' and npos not in visited:
                visited.add(npos)
                q.append( (steps-1, npos) )
    return len(plots)

plots = walk_steps(64, spos)
part1(plots)

# Part 2
# As we continue traversing the garden map, every other garden plot will be visitable
# leading to a checkerboard pattern of final locations. The input map has an interesting
# characteristic - the true directions from 'S' are all unobstructed, meaning we can
# walk N, E, S, W indefinitely. 
# When walking the map, with say 10 steps, the farthest we can go is a Manhattan distance
# of 10 from our starting pos. Regardless of where stones are placed, this will cause
# out visited garden plots to form the shape of a diamond. We rely on this shape to
# calculate how the infinite maps are filled.

STEPS = 26501365

# We first need to determine how many steps it takes to fill our map
# We find that we alternate between 7363 for odd steps and 7410 for even steps
# Pick a sufficiently large steps value, both odd and even, to get these values
odd_points = walk_steps(SIZE*2 + 1,spos)
even_points = walk_steps(SIZE*2,spos)

# Determine how big our final grid will be. Think of this as walking due East -
# since it's unobstructed.
grid_width = STEPS // SIZE - 1

# When we walk from grid to grid, our step counts will land on the same squares with
# either an odd or even step count. This means we need to know which map grids will have
# odd or even grid parity.
odd_grids = (grid_width // 2 * 2 + 1) ** 2
even_grids = ((grid_width + 1) // 2 * 2) ** 2
print(odd_grids, even_grids)

# Observation: Our target step count will take us N and a 1/2 grids away from S
# This means by starting in the center of our grid, we'll end up exactly on
# the outer edge of some other grid (when travelling in a cardinal direction)
print(STEPS % SIZE)
print(SIZE // 2)
assert STEPS % SIZE == SIZE // 2
# For these cardinal "corners", let's count how many plots would be visited
# when we enter each of those corners from their respective direction. And, again,
# since the cardinal directions are unobstructed, the most steps we can take
# is our SIZE-1. And we enter the grids from the middle of a side.
corner_N = walk_steps(SIZE-1, (spos[0],SIZE-1)) # entering from due south
corner_E = walk_steps(SIZE-1, (0,spos[1]))
corner_S = walk_steps(SIZE-1, (spos[0],0))
corner_W = walk_steps(SIZE-1, (SIZE-1,spos[1]))
print(corner_N, corner_E, corner_S, corner_W)

# The diagonals of our final diamond slice through grids in two distinct patterns.
# For example, when looking at our diagonal on the north east, we'll have one grid
# sliced into a small triangle in the grid's lower-left, and another that's most
# of the grid, except for its top-right corner. We need to figure out how many
# of these we have, as well as count how many garden plots can be visited in each.

# For the small triangles, we start at a grid corner closest to our starting position
# and only walk half of the grid SIZE.
small_NE = walk_steps(SIZE//2 - 1, (0,SIZE-1))
small_SE = walk_steps(SIZE//2 - 1, (0,0))
small_SW = walk_steps(SIZE//2 - 1, (SIZE-1,0))
small_NW = walk_steps(SIZE//2 - 1, (SIZE-1,SIZE-1))

# For the large "slices", we also start at the corner but only go as far as
# mid-way up an opposing side of the grid. For example, let's say we start at
# the bottom-left corner of a grid, we walk horizontally along the bottom edge,
# and then up the right side to the half way point. This is SIZE-1 steps to the
# right, plus SIZE//2 steps up. (SIZE-1) + SIZE//2 = 3*SIZE//2 - 1 steps
large_NE = walk_steps(3*SIZE//2 - 1, (0,SIZE-1))
large_SE = walk_steps(3*SIZE//2 - 1, (0,0))
large_SW = walk_steps(3*SIZE//2 - 1, (SIZE-1,0))
large_NW = walk_steps(3*SIZE//2 - 1, (SIZE-1,SIZE-1))

# We now have all map grids accounted for: the ones fully filled (accounting
# for odd/even parity), the cardinal corners, and the two types of grids (both
# small and large) on the diagonals.
part2(
    odd_grids * odd_points + 
    even_grids * even_points +
    corner_N + corner_E + corner_S + corner_W +
    (grid_width + 1) * (small_NE + small_SE + small_SW + small_NW) +
    grid_width * (large_NE + large_SE + large_SW + large_NW)
)
