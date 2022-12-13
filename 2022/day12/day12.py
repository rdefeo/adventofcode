#!/usr/bin/env python3

### Advent of Code - 2022 - Day 12

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
#input_nums = list(map(int,input_lines))

S = ()
E = ()
HEIGHT = len(input_lines)
WIDTH = len(input_lines[0])

grid = dict()
for y,line in enumerate(input_lines):
    for x,e in enumerate(line):
        if e == 'S':
            elevation = 1
            S = (x,y)
        elif e == 'E':
            elevation = 26
            E = (x,y)
        else:
            elevation = ord(e)-ord('a')+1
        grid[(x,y)] = elevation

# Prints the elevation grid. Path will be highlighted if supplied in 'p'
def print_grid(g,p=None):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if p and (x,y) in p:
                print(DPURPLE,end='')
            print(f"{g[(x,y)]:3}",end='')
            if p and (x,y) in p:
                print(CLEAR,end='')
        print()

# Computes all edges in the graph
#   start_node : { (weight1, neighbor1), (weight2, neighbor2), ... }
# where 'weight' is always '1', since we always take 1 step. If there was a cost
# taken for each step, say the height difference, we'd change that value
def compute_graph(g):
    graph = collections.defaultdict(set)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            for nx,ny in [(x+dx,y+dy) for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]]:
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT: # we're still in the grid, yes?
                    if grid[(nx,ny)]-grid[(x,y)] <= 1:
                        graph[(x,y)].add((1,(nx,ny))) # the cost of the step is 1
    return graph

# Dijkstra's Algorithm - basically unchanged from 2021 Day 15!
# Returns the shortest path from start to end
def dijkstra(g, start, end):
    q = [ (0, start, []) ] # path_len, node, path
    seen = set()
    path_lens = { start: 0 }
    while q:
        (plen, v1, path) = heapq.heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = [v1] + path
            if v1 == end: return (plen, path)
            for cost, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = path_lens.get(v2, None)
                next = plen + cost
                if prev is None or next < prev:
                    path_lens[v2] = next
                    heapq.heappush(q, (next, v2, path))
    return float("inf"), None

the_graph = compute_graph(grid)

# Part 1
print(S,E)
l, p = dijkstra(the_graph,S,E)
print_grid(grid,p)
part1(l)

# Part 2
shortest_len = WIDTH * HEIGHT
shortest_path = []
for start in [s for s in grid if grid[s] == 1]:
    l, p = dijkstra(the_graph,start,E)
    if l < shortest_len:
        shortest_len, shortest_path = l, p
print_grid(grid,shortest_path)
part2(shortest_len)
