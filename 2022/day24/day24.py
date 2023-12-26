#!/usr/bin/env python3

### Advent of Code - 2022 - Day 24

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
from copy import deepcopy

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

start = end = None
valley = collections.defaultdict(list)
for y, line in enumerate(input_lines):
    for x, v in enumerate(line):
        if v != '.':
            valley[(x,y)] += [v]
        if y == 0 and v == '.':
            start = (x,y)
        if y == len(input_lines)-1 and v == '.':
            end = (x,y)
print(start,end)
print(len(valley))
WIDTH = len(input_lines[0])
HEIGHT = len(input_lines)
E = start

def print_valley(v,e=None):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x,y) == e:
                print(YELLOW+'E'+CLEAR,end='')
                continue
            if (x,y) not in v:
                print(DPURPLE+'.'+CLEAR,end='')
            elif len(v[(x,y)]) == 1:
                print(CYAN+v[(x,y)][0]+CLEAR,end='')
            else:
                print(len(v[(x,y)]),end='')
        print()
    print()

# print_valley(valley,E)

def update_valley(v):
    nv = collections.defaultdict(list)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            for b in v[(x,y)]:
                if b == '#':
                    nv[(x,y)] = b
                elif b == '>':
                    if x < WIDTH-2:
                        nv[(x+1,y)] += [b]
                    else:
                        nv[(1,y)] += [b]
                elif b == '<':
                    if x > 1:
                        nv[(x-1,y)] += [b]
                    else:
                        nv[(WIDTH-2,y)] += [b]
                elif b == '^':
                    if y > 1:
                        nv[(x,y-1)] += [b]
                    else:
                        nv[(x,HEIGHT-2)] += [b]
                elif b == 'v':
                    if y < HEIGHT-2:
                        nv[(x,y+1)] += [b]
                    else:
                        nv[(x,1)] += [b]
    # print(f"updated: {len(nv)}")
    return nv

VALLEYS = [valley]
def get_valley(minutes):
    global VALLEYS
    # print(f"getting vally {minutes}")
    if minutes < len(VALLEYS):
        # print(" - found it!")
        return VALLEYS[minutes]
    # print(f"get_valley: {minutes} - {len(VALLEYS)}")
    # print(f" range( {len(VALLEYS)-1}, {minutes+1} )")
    for m in range(len(VALLEYS)-1,minutes):
        # print(f" m = {m}")
        nv = update_valley(VALLEYS[m])
        VALLEYS.append(deepcopy(nv))
    return VALLEYS[minutes]

#for m in range(4):
#    print_valley(get_valley(m))
#exit()

def in_valley(x,y):
    if 0 < x < WIDTH and 0 <= y < HEIGHT:
        return True
    return False

def bfs(m, s, e):
    q = collections.deque()
    seen = set()
    # dist, position, curr_valley
    q.append( (m, s) )
    
    while q:
        minutes, (x,y) = q.popleft()
        if (minutes,(x,y)) in seen:
            continue
        seen.add((minutes,(x,y)))
        
        if (x,y) == e:
            return minutes

        # print(f"min: {minutes}, E: {(x,y)}")
        
        nv = get_valley(minutes+1)
        # print_valley(nv,(x,y))
        # we have to move - check directions
        if (x,y+1) not in nv and in_valley(x,y+1):
            q.append((minutes+1,(x,y+1)))
        if (x+1,y) not in nv and in_valley(x+1,y):
            q.append((minutes+1,(x+1,y)))
        if (x,y-1) not in nv and in_valley(x,y-1):
            q.append((minutes+1,(x,y-1)))
        if (x-1,y) not in nv and in_valley(x-1,y):
            q.append((minutes+1,(x-1,y)))
        if (x,y) not in nv: # no blizzard here, waiting is an option
            q.append((minutes+1,(x,y)))
        if len(q) % 100 == 0:
            print(f"q len = {len(q)}")
        # break

m1 = bfs(0,start,end)
part1(m1)
m2 = bfs(m1,end,start)
m3 = bfs(m2,start,end)
print(m1,m2,m3)
part2(m3)
