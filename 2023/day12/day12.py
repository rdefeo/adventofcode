#!/usr/bin/env python3

### Advent of Code - 2023 - Day 12

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

def find_arrangements(line, p2=False):
    springs, broken = line.split()
    broken = list(map(int,broken.split(',')))

    if p2:
        springs = '?'.join([springs for _ in range(5)])
        broken = broken * 5
    
    seen = dict()
    def find_count(s, b, bsize):
        # s is our index into springs
        # b is our index into our broken spring block list
        # bsize is the current size of broken spring block we're in
        
        if (s,b,bsize) in seen:
            return seen[(s,b,bsize)]
        
        # If we've reached the end of our spring list, check if we're "done"
        if s == len(springs):
            # If we've finished checking broken blocks and
            # there's no current block, then we must have a valid arrangement!
            if b == len(broken) and bsize == 0:
                return 1
            # If we're on the last broken block, and that block is the right size
            if b == len(broken)-1 and bsize == broken[-1]:
                return 1
            return 0
        
        arr = 0
        if springs[s] in '.?': # either a working or unknown spring
            if bsize == 0:
                # We're not currently in a block of broken springs,
                # so just move forward to the next spring
                arr += find_count(s+1,b,0)
            else:
                # We're in a block of broken springs, but ran out of spring blocks! Not valid
                if b == len(broken):
                    return 0
                # We've found a block of broken springs the right size,
                # move forward to the next spring and the next spring block
                if bsize == broken[b]:
                    arr += find_count(s+1,b+1,0)
        if springs[s] in '#?': # either a broken or unknown spring
            arr += find_count(s+1,b,bsize+1)
            
        seen[(s,b,bsize)] = arr
        return arr
    return find_count(0,0,0)
    
part1(sum(find_arrangements(line) for line in input_lines))
part2(sum(find_arrangements(line,True) for line in input_lines))
