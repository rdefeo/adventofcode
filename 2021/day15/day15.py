#!/usr/bin/env python3

### Advent of Code - 2021 - Day 15

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

Y = len(input_lines)
X = len(input_lines[0])
cavern = {(x,y):int(r) for y,line in enumerate(input_lines) for x,r in enumerate(line)}

def print_grid(g,p=None,w=X,h=Y):
    ''' Prints the grid, highlighting the optional path '''
    for y in range(h):
        for x in range(w):
            if p and (x,y) in p:
                print(DPURPLE,end='')
            print(g[(x,y)],end='')
            if p and (x,y) in p:
                print(CLEAR,end='')
        print('')

# Computes all edges in the graph:
#   start_node : { (weight1,neighbor1), (weight2,neighbor2), ... }
def compute_graph(g):
    graph = collections.defaultdict(set)
    w = max([mx for mx,_ in g.keys()])+1
    h = max([my for _,my in g.keys()])+1
    for y in range(h):
        for x in range(w):
            for nx,ny in [(x+dx,y+dy) for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]]:
                if 0 <= nx < w and 0 <= ny < h:
                    graph[(x,y)].add((g[(nx,ny)],(nx,ny)))
                    # graph[(nx,ny)].add((g[(x,y)],(x,y)))
    return graph

# Dijkstra's Algorithm - basically unchanged from 2019 Day 20 !
# Returns lowest cost, path to end
def dijkstra(g, start, end):
    q = [ (0, start, []) ] # cost, node, path
    seen = set()
    risks = { start: 0 } # min risk per node
    while q:
        (risk, v1, path) = heapq.heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = [v1] + path
            if v1 == end: return (risk, path)
            for cost, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = risks.get(v2, None)
                next = risk + cost
                if prev is None or next < prev:
                    risks[v2] = next
                    heapq.heappush(q, (next, v2, path))
    return float("inf"), None

# Part 1
path = dijkstra(compute_graph(cavern),(0,0),(X-1,Y-1))
# print(path)
# print_grid(cavern,path[1])
part1(path[0])

# Part 2 - expand the 'cavern' grid by 5x
for y in range(Y):
    for x in range(X):
        r = cavern[(x,y)]
        for j in range(5):
            for i in range(5):
                nr = (r + i + j)
                while nr > 9:
                    nr -= 9
                cavern[(x+X*i,y+Y*j)] = nr

path = dijkstra(compute_graph(cavern),(0,0),(X*5-1,Y*5-1))
# print(path)
# print_grid(cavern,path[1],X*5,Y*5)
part2(path[0])
