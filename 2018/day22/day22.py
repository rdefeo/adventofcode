#!/usr/bin/env python3

### Advent of Code - 2018 - Day 22

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
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

depth = int(input_lines[0].split(' ')[1])
tx,ty = list(map(int,input_lines[1].split(' ')[1].split(',')))

print(depth)
print(tx,ty)

ROCKY, WET, NARROW = 0, 1, 2
NEITHER, TORCH, CLIMB = 0, 1, 2

# tools allowed per region
# ROCKY  -> TORCH, CLIMB    (0 -> 1,2)
# WET    -> NEITHER, CLIMB  (1 -> 0,2)
# NARROW -> NEITHER, TORCH  (2 -> 0,1)
# this means that for any tool we're holding, we can't enter a region
# that has the same region type

def rtype(e):
    return {0:'.', 1:'=', 2:'|'}[e%3]

eseen = dict()
def erosion(x,y):
    if (x,y) in eseen:
        return eseen[(x,y)]
    e = (geologic(x,y) + depth) % 20183
    eseen[(x,y)] = e
    return e

def geologic(x,y):
    if x == 0 == y:
        return 0
    if x == tx and y == ty:
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return erosion(x-1,y) * erosion(x,y-1)

# depth = 510
# tx,ty = 10,10
risk = 0
for y in range(ty+1):
    for x in range(tx+1):
        if x == 0 == y:
            print('M',end='')
        elif x == tx and y == ty:
            print('T',end='')
        else:
            e = erosion(x,y)
            risk += e%3
            print(rtype(e),end='')
            # print(e%3,end='')
    print('')
print('')

part1(risk)

def neighbors(x,y):
    directions = [(1,0),(0,1),(-1,0),(0,-1)] # R,D,L,U
    return [(x+d[0],y+d[1]) for d in directions]

heap = [(0, 0, 0, TORCH)] # time, x, y, equip in use (we start w/ TORCH)
visited = { (0,0,TORCH): 0 } # pos, equip used : time

def visit_next(time, x, y, eq, heap):
    for nx,ny in neighbors(x,y):
        if nx < 0 or ny < 0: # out of bounds
            continue
        if erosion(nx,ny)%3 == equip: # holding wrong tool
            continue
        # we've been to n before, but faster
        if (nx,ny,equip) in visited and visited[(nx,ny,equip)] <= time:
            continue
        visited[(nx,ny,equip)] = time
        heappush(heap,(time,nx,ny,equip))

while True:
    time, x, y, equip = heappop(heap)
   
    # Have we reached the target?
    if (x,y) == (tx,ty) and equip == TORCH:
        part2(time)
        break

    # Try moving to one of our neighbors with the equip we have in hand
    time += 1
    visit_next(time,x,y,equip,heap)

    # Now try using other equip
    time += 7
    equip = 3 - equip - erosion(x,y)%3
    visit_next(time,x,y,equip,heap)

