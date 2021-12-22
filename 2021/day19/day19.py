#!/usr/bin/env python3

### Advent of Code - 2021 - Day 19

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

scanners = []
S = finput.split('\n\n')
for i in S:
    s = i.split('\n')[1:]
    scanners.append([list(map(int,b.split(','))) for b in s])

# rotate p around X axis by n * 90deg
def rotX(p,n):
    for _ in range(n):
        p = [p[0],-p[2],p[1]]
    return p

def rotY(p,n):
    for _ in range(n):
        p = [p[2],p[1],-p[0]]
    return p

def rotZ(p,n):
    for _ in range(n):
        p = [p[1],-p[0],p[2]]
    return p

# return all 4 rotations around Z axis
def rotations(p):
    return [p, rotZ(p,1), rotZ(p,2), rotZ(p,3)]

# returns all 24 orientations for a given point
def orientations(p):
    o = []
    o += rotations(p)
    o += rotations(rotX(p,1))
    o += rotations(rotX(p,2))
    o += rotations(rotX(p,3))
    o += rotations(rotY(p,1))
    o += rotations(rotY(p,3))
    return o

# directional dx, dy, dz between two beacons
def compute_beacon_dist(p,q):
    return (p[0]-q[0]), (p[1]-q[1]), (p[2]-q[2])

# Manhattan distance, for Part 2
def compute_abs_dist(p,q):
    return abs(p[0]-q[0]) + abs(p[1]-q[1]) + abs(p[2]-q[2])

def compute_scanner_dist_pairs(s):
    return {compute_beacon_dist(p,q):(p,q) for p in s for q in s if p != q}

def merge_scanners(dest,src,offset):
    for b in src:
        nb = [b[0]+offset[0],b[1]+offset[1],b[2]+offset[2]]
        if nb not in dest:
            dest.append(nb)
    return dest

# generate all 24 orientations for every scanner
# SP[ 'scanner' ][ 'orientation' ] = [ 'beacon 1', 'beacon 2', ... ]
SO = [[[] for _ in range(24)] for _ in range(len(scanners))]
for i in range(len(scanners)):
    if i == 0: continue # don't need this for scanner 0
    for p in scanners[i]:
        for j,o in enumerate(orientations(p)):
            SO[i][j].append(o)

# compute the dist pairs for every beacon in every 24 orientations for every scanner
# DP[ 'scanner' ][ 'orientation' ] = { 'dist': ('beacon 1','beacon 2') }
DP = [[[] for _ in range(24)] for _ in range(len(scanners))]
for s in range(len(scanners)):
    if s == 0: continue # don't need this for scanner 0
    for o in range(len(SO[s])):
        DP[s][o] = compute_scanner_dist_pairs(SO[s][o])

# scanner 0 sets our orientation, all others should match
final_scan = scanners[0]

# Part 1
merged = {0}
scanner_offsets = [(0,0,0)]
while True:
    for s in range(len(scanners)):
        if s in merged: continue
        final_dist_pairs = compute_scanner_dist_pairs(final_scan)
        # for every orientation, find which one produces the most matching pairs
        pair_match = 0
        orientation = 0
        offset = []
        for o in range(len(DP[s])):
            pair_matches = {d for d in DP[s][o] if d in final_dist_pairs}
            if len(pair_matches) > pair_match:
                pair_match = len(pair_matches)
                orientation = o
                d = next(iter(pair_matches)) # just grab any one to compute offset, since they're all the same
                offset = [final_dist_pairs[d][0][i]-DP[s][o][d][0][i] for i in range(3)]
        if pair_match: # this could be 0, which means no orientation of scanner s overlaps
            # translate its points to the origin and combine with final
            final_scan = merge_scanners(final_scan,SO[s][orientation],offset)
            merged.add(s)
            scanner_offsets.append(offset)
    if len(merged) == len(scanners):
        break
part1(len(final_scan))

# Part 2
mdist = 0
for i in scanner_offsets:
    for j in scanner_offsets:
        if i == j: continue
        mdist = max(mdist,compute_abs_dist(i,j))
part2(mdist)

