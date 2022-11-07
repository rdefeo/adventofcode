#!/usr/bin/env python3

### Advent of Code - 2016 - Day 17

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import hashlib
from heapq import heappush, heappop

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


def neighbors(x,y,path):
    hpath = hashlib.md5(path.encode()).hexdigest()[:4]
    path_letter = 'UDLR'
    directions = [(0,-1),(0,1),(-1,0),(1,0)]
    n = []
    for i,h in enumerate(hpath):
        if h in 'bcdef':
            d = directions[i]
            n.append( ((x+d[0],y+d[1]),path_letter[i]) )
    return n

# 4x4 maze, we start in top-left, vault in bottom-right
tx,ty = 3,3

passcode = 'ihgpwlah'
passcode = 'kglvqrro'
passcode = 'ulqzkmiv'
passcode = 'awrkjxxr' # my input

part_1 = False
heap = [(0,passcode,(0,0))] # dist,path,(x,y) - start at 0,0
paths = []
while heap:
    dist,path,(x,y) = heappop(heap)
    dist += 1
    for (nx,ny),np in neighbors(x,y,path):
        if not (0 <= nx < 4 and 0 <= ny < 4): # out of maze
            continue
        if (nx,ny) == (tx,ty):
            paths.append(path+np)
            if part_1:
                part1(path[8:]+np)
                quit()
        else:
            heappush(heap,(dist,path+np,(nx,ny)))
# print(paths)
part2(max([len(p)-len(passcode) for p in paths]))
