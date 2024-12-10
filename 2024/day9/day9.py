#!/usr/bin/env python3

### Advent of Code - 2024 - Day 9

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

fs = finput
id = 0
disk = [] # raw data, every block
files = [] # (id, offset, length)
frees = [] # (None, offset, length)
offset = 0
for i,b in enumerate(fs):
    b = int(b)
    if i%2 == 0:
        files.append((id,offset,b))
        for _ in range(b):
            disk.append(id)
        id += 1
    else:
        frees.append((None,offset,b))
        for _ in range(b):
            disk.append(None)
    offset += b
orig_disk = disk.copy() # save for later

def checksum(d):
    c = 0
    for i,v in enumerate(d):
        if v is not None:
            c += i*v
    return c

# Part 1 - straight-forward solution
# Using two indices, traverse from beginning and end and move items
s, e = 0, len(disk)-1
while s < len(disk) and s <= e:
    while disk[s] != None:
        s += 1
    while disk[e] == None:
        e -= 1
    if e <= s:
        break
    disk[s] = disk[e]
    disk[e] = None
    s += 1
    e -= 1

part1(checksum(disk))

# Part 2
disk = orig_disk
for f in range(len(files)-1,0,-1): # can skip first, since it's already 0-indexed
    for fr in range(0,len(frees)):
        # if free spot is before the file and this file can fit into the free spot 
        if frees[fr][1] < files[f][1] and files[f][2] <= frees[fr][2]:
            o = frees[fr][1]
            for i in range(files[f][2]):
                disk[o+i] = files[f][0] # copy id into new location
                disk[files[f][1]+i] = None # clear old location
            # recompute all frees - effectively merging any consecutive empty spots
            # oof, there has to be a better way - pypy makes quick work of this in ~3s
            frees = []
            flen = 0
            start = None
            for i, v in enumerate(disk):
                if v == None:
                    if start == None:
                        start = i
                    flen += 1
                else:
                    if start != None:
                        frees.append((None,start,flen))
                        start = None
                        flen = 0
            break
part2(checksum(disk))
