#!/usr/bin/env python3

### Advent of Code - 2023 - Day 23

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import heapq

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
# Not the best code or fastest (by a long shot), but it works! Simple BFS for this part

NORTH, EAST, SOUTH, WEST = (0,-1), (1,0), (0,1), (-1,0)

grid = input_lines
HEIGHT = len(grid)
WIDTH = len(grid[0])

START = (1, 0)
END = (WIDTH-2,HEIGHT-1)
sx, sy = START

def find_paths():
    """ Simple BFS to reach the end of the maze. Keep track of our step counts
    as negative numbers so we can use a priority queue. Also, don't walk up slopes. """
    v = set()
    v.add((0,0))
    q = [ (0, sx, sy, v) ]
    paths = []
    print(WIDTH-2,HEIGHT-1)
    seen = set()

    while q:
        steps, x, y, visited = heapq.heappop(q)

        # We've reached the end, record our step count
        if (x,y) == END:
            paths.append(-steps)
            continue
        
        if (steps,x,y) in seen:
            continue
        seen.add((steps,x,y))

        came_from = None
        for dx,dy in [NORTH, EAST, SOUTH, WEST]:
            if came_from == (dx,dy): continue
            nx, ny = x+dx, y+dy
            if (nx,ny) in visited: continue

            next_g = grid[ny][nx]
            if next_g == '#': continue

            # Don't walk up slopes
            if next_g == 'v' and (dx,dy) == NORTH: continue
            if next_g == '<' and (dx,dy) == EAST: continue
            if next_g == '^' and (dx,dy) == SOUTH: continue
            if next_g == '>' and (dx,dy) == WEST: continue

            visited.add((nx,ny))
            heapq.heappush( q, (steps-1, nx, ny, visited.copy()) )
    return paths

paths = find_paths()
part1(max(paths))

# Part 2
# The BFS solution from Part 1 was never going to complete in time for this part. So instead,
# we use a DFS approach to traverse the map, but not at every x,y. We generate a graph with
# intersections (and START / END) as our nodes, and the edges are weighted by distance.
# I'm sure the was a way to merge this solution with Part 1, but this works.

def get_possible_dirs(p):
    for dx,dy in [NORTH, EAST, SOUTH, WEST]:
        nx, ny = p[0]+dx, p[1]+dy
        if nx < 0 or nx > WIDTH-1 or ny < 0 or ny > HEIGHT-1:
            continue
        if grid[ny][nx] == '#':
            continue
        yield ((nx,ny),(-dx,-dy))

# Intersections in our map are places where you can walk in more than 2 directions
# Brute-force find all in the input map
def find_intersections():
    ints = set()
    for y, line in enumerate(grid):
        for x, g in enumerate(line):
            if g == '#': continue
            dirs = 0
            for dx,dy in [NORTH, EAST, SOUTH, WEST]:
                nx, ny = x+dx, y+dy
                if nx < 0 or nx > WIDTH-1 or ny < 0 or ny > HEIGHT-1: continue
                if grid[ny][nx] == '#': continue
                dirs += 1
            if dirs > 2:
                ints.add((x,y))
        # break
    return ints

all_intersections = find_intersections()
all_ints = all_intersections.copy()
all_ints.add(START)
all_ints.add(END)

# Build a weighted graph of our intersections with distances between, including START and END
# Uses a simple BFS algorithm
graph = collections.defaultdict(dict) # intA -> intB -> dist
q = [ (START,0) ]
seen = set()
while q:
    p, dist = q.pop(0)
    
    if p in seen: continue
    seen.add(p)

    for poss,came_from in get_possible_dirs(p):
        # walk this path until the next intersection
        ndist = dist + 1 # as we are now standing on the first spot of a new path
        while poss not in all_ints:
            for dx,dy in [NORTH, EAST, SOUTH, WEST]:
                if (dx,dy) == came_from: continue
                nx, ny = poss[0]+dx, poss[1]+dy
                if nx < 0 or nx > WIDTH-1 or ny < 0 or ny > HEIGHT-1: continue
                if grid[ny][nx] == '#': continue
                ndist = ndist + 1
                came_from = (-dx,-dy)
                poss = (nx,ny)
                break
        graph[p][poss] = ndist
        graph[poss][p] = ndist
        q.append( (poss,0) )
# print(graph)

def max_dist2(start, visited, dist):
    """ DFS approach to traverse our graph, from START and finding all possible paths. """
    nvisited = visited | {start}
    dists = []
    if start == END:
        return dist
    for b, bdist in graph[start].items():
        if b in nvisited: continue
        dists.append(max_dist2(b,nvisited,dist+bdist))
    if not dists: return 0
    return max(dists)
part2(max_dist2(START,set(),0))
