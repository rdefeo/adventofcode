#!/usr/bin/env python3

### Advent of Code - 2024 - Day 16

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

maze = dict()
for y, row in enumerate(input_lines):
    for x, c in enumerate(row):
        if c == 'S':
            S = (x,y)
        elif c == 'E':
            E = (x,y)
        maze[(x,y)] = c
H, W = len(input_lines), len(input_lines[0])

def turnR(d):
    return (-d[1],d[0])
def turnL(d):
    return (d[1],-d[0])

def print_maze(maze,path=None):
    for y in range(H):
        for x in range(W):
            if path and (x,y) in path:
                print('O',end='')
            else:
                print(maze[(x,y)],end='')
        print()
    print()

scores = [] # score, path
queue = [(S, 0, (1,0), [S])] # position, score, dir facing, path
visited = dict()
while queue:
    p, s, d, path = queue.pop(0)
    if p == E:
        scores.append((s,path))
        continue
    if maze[p] == '#':
        continue
    if (p,d) in visited and s > visited[(p,d)]:
        continue
    visited[(p,d)] = s
    
    # try moving in current direction
    np = (p[0]+d[0],p[1]+d[1])
    queue.append((np, s+1, d, path + [np]))
    # try moving in the left direction
    nd = turnL(d)
    np = (p[0]+nd[0],p[1]+nd[1])
    queue.append((np, s+1001, nd, path + [np]))
    # try moving in the right direction
    nd = turnR(d)
    np = (p[0]+nd[0],p[1]+nd[1])
    queue.append((np, s+1001, nd, path + [np]))

min_score = min(s for s,_ in scores)
part1(min_score)

best = set()
for s,path in scores:
    if s == min_score:
        best.update(path)
#print_maze(maze,best)
part2(len(best))