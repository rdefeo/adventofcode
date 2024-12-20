#!/usr/bin/env python3

### Advent of Code - 2024 - Day 20

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

track = dict()
for y, row in enumerate(input_lines):
    for x, c in enumerate(row):
        if c == 'S':
            S = (x,y)
        elif c == 'E':
            E = (x,y)
        track[(x,y)] = c
H, W = len(input_lines), len(input_lines[0])

def print_track(track,path = None,cheats = None):
    for y in range(H):
        for x in range(W):
            if cheats and (x,y) in cheats:
                print('1',end='')
            elif path and (x,y) in path:
                print('O',end='')
            else:
                print(track[(x,y)],end='')
        print()
    print()

# Simple flood fill to find the path in the maze. We know it's a single path
# with no branching so we don't need to find shortest, etc.
def find_full_path(s, e, track):
    path = [s]
    seen = set(path)
    while s != e:
        for dx, dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            np = (s[0]+dx,s[1]+dy)
            if track[np] == '#' or np in seen: continue
            seen.add(np)
            path.append(np)
            s = np
            break
    return path

path = find_full_path(S,E,track)
# Invert our path to determine how many picoseconds it takes to reach each step on the path
path_times = {p:i for i,p in enumerate(path)}

# Walk the existing path and try to cheat in up to cheat_len steps
def find_cheats(track, path, cheat_len = 20, target_savings = 100):
    num_cheats = 0
    for p in path:
        for dy in range(-cheat_len, cheat_len+1):
            for dx in range(-cheat_len, cheat_len+1):
                steps = abs(dx) + abs(dy)
                if steps > cheat_len: 
                    continue
                np = (p[0]+dx,p[1]+dy)
                if np not in track or track[np] == '#' or path_times[np] <= path_times[p]: continue
                savings = path_times[np] - (path_times[p] + steps)
                if savings >= target_savings:
                    num_cheats += 1
    return num_cheats

part1(find_cheats(track, path, 2, 100))

part2(find_cheats(track, path, 20, 100))
