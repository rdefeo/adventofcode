#!/usr/bin/env python3

### Advent of Code - 2020 - Day 20

import sys
import requests
import re
import math
import itertools
import functools
import os
import collections
from functools import lru_cache

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as one long string and as an array of lines
inputfile = 'input'
if len(sys.argv) == 2:
    inputfile = sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
#input_nums = list(map(int,input_lines))
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

p1 = 0
p2 = 0

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

def create_mirrors(grid):
    mirrors = [grid]
    mirrors.append(grid[::-1])
    mirrors.append([r[::-1] for r in grid])
    mirrors.append([r[::-1] for r in grid][::-1])
    return mirrors

# rotates grid left
def create_rotations(grid):
    rot = [grid]
    last = grid
    for _ in range(3):
        grid = [l[:] for l in grid]
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                grid[x][y] = last[len(grid)-y-1][x]
        last = grid
        rot.append(grid)
    return rot


class Tile:
    def __init__(self,id):
        self.id = id
        self.rows = []
        self.options = []
        self.edges = []

    def compute_orientations(self):
        # compute all options
        all_grids = []
        
        mirrors = create_mirrors(self.rows)
        for m in mirrors:
            all_grids.extend(create_rotations(m))

        # after flipping and creating the rotations of each
        # we may have some duplicate grids, get rid of them
        for e in all_grids:
            if e not in self.options:
                self.options.append(e)

        def get_edges(grid):
            top = grid[0]
            right = ''.join(l[-1] for l in grid)
            bottom = grid[-1]
            left = ''.join(l[0] for l in grid)
            return (top,right,bottom,left)
        # create the list of edges (T,R,B,L) for every possible
        # tile orientation
        for o in self.options:
            self.edges.append(get_edges(o))
        
    # def __repr__(self):
    #     repr = f"Tile {self.id}:\n"
    #     for r in self.rows:
    #         repr += r+'\n'
    #     return repr

tiles = []
intiles = input.split('\n\n')
#print(intiles)
for it in [x.split('\n') for x in intiles]:
    m = re.match(r"Tile (\d+):",it[0])
    t = Tile(int(m.group(1)))
    for l in it[1:]:
        t.rows.append(list(l))
    t.compute_orientations()                
    tiles.append(t)

dim = math.isqrt(len(intiles))

def can_place(grid,t,e,x,y):
    """Given a (grid) state, a tile (t), an index (e) into the list of
    tile orientations, and an (x), (y) location, see if that tile
    can fit, by checking all edges with its neighbors"""
    # look above
    if y > 0 and grid[x][y-1]:
        above,i = grid[x][y-1]
        if above.edges[i][BOTTOM] != t.edges[e][TOP]:
            return False
    # look right
    if x < dim-1 and grid[x+1][y]:
        right,i = grid[x+1][y]
        if right.edges[i][LEFT] != t.edges[e][RIGHT]:
            return False
    # look down
    if y < dim-1 and grid[x][y+1]:
        below,i = grid[x][y+1]
        if below.edges[i][TOP] != t.edges[e][BOTTOM]:
            return False
    # look left
    if x > 0 and grid[x-1][y]:
        left,i = grid[x-1][y]
        if left.edges[i][RIGHT] != t.edges[e][LEFT]:
            return False
    return True

def create_tile_grid(grid,x,y,seen):
    """Starting at position (x),(y), iterate over the tiles
    and try placing each one, and then recurse using the next
    position (nx),(ny). Keep track of which tiles were placed
    with the set (seen)"""
    if y == dim:
        return grid
    nx, ny = x+1, y
    if nx == dim:
        nx = 0
        ny += 1
    for t in tiles:
        if t.id in seen:
            continue
        seen.add(t.id)
        for i,_ in enumerate(t.options):
            if can_place(grid,t,i,x,y):
                grid[x][y] = (t,i)
                newg = create_tile_grid(grid,nx,ny,seen)
                if newg is not None:
                    return newg
        seen.remove(t.id)
    grid[x][y] = None
    return None

# Part 1
grid = [[None for _ in range(dim)] for _ in range(dim)]
g = create_tile_grid(grid,0,0,set())

# multiply the Tile ids at the corners
print(g[0][0][0].id,g[dim-1][0][0].id,g[dim-1][dim-1][0].id,g[0][dim-1][0].id)
part1(g[0][0][0].id*g[dim-1][0][0].id*g[dim-1][dim-1][0].id*g[0][dim-1][0].id)

tsize = len(tiles[0].rows)

# Part 2
def merge_tiles(grid):
    """combine the tiles, after removing the borders on each"""
    merge = []
    for sy in range(dim):
        for y in range(1,tsize-1):
            merge.append([])
            for sx in range(dim):
                t,i = grid[sx][sy]
                merge[sy*(tsize-2)+y-1] += t.options[i][y][1:-1]
    return merge

mg = merge_tiles(g)
def print_sea(sea):
    for y in sea:
        print(''.join(x for x in y))
print_sea(mg)

def count_waves(sea):
    waves = 0
    for y in sea:
        waves += ''.join(x for x in y).count('#')
    return waves

monster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""
mc = [(0,1),(1,2),                      # tail
    (4,2),(5,1),(6,1),(7,2),            # hump
    (10,2),(11,1),(12,1),(13,2),        # hump
    (16,2),(17,1),(18,0),(18,1),(19,1)] # head

all_seas = []
mirrors = create_mirrors(mg)
for m in mirrors:
    all_seas.extend(create_rotations(m))

for s in all_seas:
    monsters = []
    sea = s[:]
    for y in range((tsize-2)*dim-3):        # monster is 3 rows tall
        for x in range(0,(tsize-2)*dim-20): # and 20 cols wide
            found = True
            for mx,my in mc:
                if sea[y+my][x+mx] != '#':
                    found = False
                    break
            if found:
                monsters.append((x,y))
    if len(monsters) > 0:
        print(f"found {len(monsters)}")
        for m in monsters:
            for mx,my in mc:
                sea[m[1]+my][m[0]+mx] = GREEN+'O'+CLEAR
        print_sea(sea)
        part2(count_waves(sea))
        quit()

