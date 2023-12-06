#!/usr/bin/env python3

### Advent of Code - 2023 - Day 5

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
#input_nums = list(map(int,input_lines))

data = finput.split('\n\n')

seeds = list(map(int,data[0].split(': ')[1].split()))
#print(seeds)

class Range:
    def __init__(self, dest, source, length):
        self.dst = int(dest)
        self.src = int(source)
        self.len = int(length)
        self.end = self.src + self.len - 1
    def convert(self, s):
        return self.dst + (s - self.src)
    def __repr__(self):
        return f"{self.src}-{self.src+self.len-1}"
    
class Map:
    def __init__(self,start,end):
        self.name = f"{start} to {end}"
        self.ranges = []
    def get_range_index(self, seed):
        for i in range(len(self.ranges)):
            if seed <= self.ranges[i].end:
                return i
        return len(self.ranges) # 1 beyond our list!
    def finalize_ranges(self):
        # sort the ranges by src, but then insert non-transforming ranges, as well as
        # the beginning range (0-n). This should make our later code a little
        # simpler when finding / iterating over ranges
        self.ranges = sorted(self.ranges,key=lambda r: r.src)
        new_ranges = []
        for i in range(0,len(self.ranges)-1):
            new_ranges.append(self.ranges[i])
            if self.ranges[i].end + 1 < self.ranges[i+1].src:
                # we have a gap between mapping ranges, insert a Range that
                # doesn't do any transforms (i.e. src == dst)
                new_ranges.append(Range(self.ranges[i].end+1,self.ranges[i].end+1,self.ranges[i+1].src-self.ranges[i].end-1))
        new_ranges.append(self.ranges[-1])
        # prepend the zero range
        if new_ranges[0].src > 0:
            new_ranges.insert(0,Range(0,0,new_ranges[0].src))
        self.ranges = new_ranges
        
    def print(self):
        print(f"{self.name}: ", end='')
        for m in self.ranges:
            print(f"({m.dst},{m.src},{m.len})", end=', ')
        print()

# Parse input data
maps = []
for m in data[1:]:
    m = m.split()
    name = m[0]
    names = name.split()[0].split('-')
    start, end = names[0], names[-1]
    maps.append(Map(start,end))
    for i in range(0,len(m[2:]),3):
        dst, src, rlen = m[2+i:2+i+3]
        maps[-1].ranges.append(Range(dst,src,rlen))
    maps[-1].finalize_ranges()
    
# Part 1
# For each seed, run it through the mappings, and record the min location result
min_seed = float("inf")
for s in seeds:
    for m in maps:
        for r in m.ranges:
            if r.src <= s <= r.end:
                s = r.convert(s)
                break
    min_seed = min(min_seed, s)
part1(min_seed)

# Part 2
# For our input list of seed ranges, determine how that range will transform
# when going through one layer of the mappings. It's possible that the range will
# not change, or be split (maybe more than once!) into more ranges. This will
# give us a new list of ranges. When we're all the way through every map,
# we'll have a final list of ranges - our result is the min value of the lowest range

seeds = sorted([(seeds[i],seeds[i]+seeds[i+1]-1) for i in range(0,len(seeds),2)])
#print(f"{seeds=}")
for m in maps:
    #print(m.name,seeds)
    new_seeds = []
    for seed in seeds:
        r_start = m.get_range_index(seed[0])
        r_end = m.get_range_index(seed[1])
        if r_start == len(m.ranges) and r_end == len(m.ranges):
            #print(f"{seed} is outside last range {m.ranges[-1]} - no transform of numbers")
            new_seeds.append(seed)
            continue
        if r_start == r_end:
            #print(f"{seed} is contained within range {r_start}: {m.ranges[r_start]}, converting")
            r = m.ranges[r_start]
            new_seeds.append((r.convert(seed[0]),r.convert(seed[1])))
            continue
        start = seed[0]
        while r_end-r_start > 0: # we're still spanning ranges
            #print(f"{seed} spans ranges {r_start} to {r_end}")
            r = m.ranges[r_start]
            new_seeds.append((r.convert(start),r.convert(r.end)))
            r_start += 1
            if r_start < len(m.ranges):
                start = m.ranges[r_start].src
        #print(f"{r_start}-{r_end}: {seed}")
        if r_end == len(m.ranges):
            new_seeds.append((m.ranges[-1].end+1,seed[1]))
        else:
            new_seeds.append((m.ranges[r_start].convert(m.ranges[r_start].src),m.ranges[r_end].convert(seed[1])))
    seeds = new_seeds
    #print()

final_ranges = sorted(seeds,key=lambda x: x[0])
part2(final_ranges[0][0])
