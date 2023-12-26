#!/usr/bin/env python3

### Advent of Code - 2023 - Day 13

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

patterns = [pattern.split('\n') for pattern in finput.split('\n\n')]

"""
maybe create a folder method, that can operate in either direction
it will try to fold a grid at each "row" or "col" and return the location of the fold
"""

def transpose(pattern):
    return [''.join(list(x)) for x in zip(*pattern)]

def find_fold(pattern, old_fold=None):
    """ For all possible fold/reflection lines, reverse the "top" rows and
    compare to the bottom rows. Ensure that they are of equal/min size.
    If we are given an old_fold value, then keep searching for a new fold value. """
    for f in range(1,len(pattern)):
        # get the items before index f and compare to those after
        fm = min(f, len(pattern)-f)
        top = pattern[f-fm:f][::-1]
        bot = pattern[f:f+fm]
        if all(top[i] == bot[i] for i in range(len(top))):
            if not old_fold or f != old_fold:
                return f
    return None

def data_split(data, n):
    return [data[i:i+n] for i in range(0,len(data),n)]

p1_summary = 0
p2_summary = 0
smudges = 0
for pattern in patterns:
    # print(pattern)
    vfold, hfold = None, None
    vfold = find_fold(transpose(pattern))
    if vfold:
        p1_summary += vfold
    else:
        hfold = find_fold(pattern)
        p1_summary += 100 * hfold

    # try to find the smudge by flipping every single square and trying to find a new fold
    orig_pattern = ''.join(pattern)
    for p in range(len(pattern) * len(pattern[0])):
        new_pattern = orig_pattern[:p] + ('.' if orig_pattern == '#' else '#') + orig_pattern[p+1:]
        new_pattern = data_split(new_pattern, len(pattern[0]))

        nvfold = find_fold(transpose(new_pattern), vfold)
        if nvfold:
            p2_summary += nvfold
            smudges += 1
            break
        nhfold = find_fold(new_pattern, hfold)
        if nhfold:
            p2_summary += 100 * nhfold   
            smudges += 1
            break
part1(p1_summary)
if smudges != len(patterns):
    print(f"{smudges=} != {len(patterns)=}")
part2(p2_summary)
