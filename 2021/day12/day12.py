#!/usr/bin/env python3

### Advent of Code - 2021 - Day 12

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

graph = collections.defaultdict(set)
for line in input_lines:
    l,r = line.split('-')
    graph[l].add(r)
    graph[r].add(l)

def find_paths(s,e,p2):
    paths = 0
    queue = [(s,{s},'')] # current node, seen lowecase, node seen twice
    while queue:
        node, seen, twice = queue.pop(0)
        for n in graph[node]:
            if n.isupper():
                queue.append( (n, seen, twice) )
            elif n.islower() and n != 'start':
                if n == e: # reached end, increment path count
                    paths += 1
                elif n not in seen:
                    queue.append( (n, seen | {n}, twice) )
                elif p2 and twice == '':
                    queue.append( (n, seen | {n}, n) )
    return paths

part1(find_paths('start','end',False))
part2(find_paths('start','end',True))
