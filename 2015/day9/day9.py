#!/usr/bin/env python3

### Advent of Code - 2015 - Day 9

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache

sys.path.append('../../python/')
from aoc_utils import *
import heapq

# read input data file as one long string and as an array of lines
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
finput = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in finput.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

# Setup the graph based on the edges in the input
graph = collections.defaultdict(dict)
for e in input_lines:
    s = e.split()
    graph[s[0]][s[2]] = int(s[-1])
    graph[s[2]][s[0]] = int(s[-1])

def tsp(g,s,part_2):
    nodes = list(g.keys())
    nodes.remove(s)
    dist = 0 if part_2 else 99999999
    for p in itertools.permutations(nodes):
        curr_dist = 0
        k = s
        for n in p:
            curr_dist += g[k][n]
            k = n
        # curr_dist += g[k][s] # dist back to starting node
        dist = max(dist,curr_dist) if part_2 else min(dist,curr_dist)
    return dist

# Part 1
def solve(part_2=False):
    dists = []
    for s in graph.keys():
        path = tsp(graph,s,part_2)
        dists.append(path)
    return dists

part1(min(solve()))
part2(max(solve(True)))

