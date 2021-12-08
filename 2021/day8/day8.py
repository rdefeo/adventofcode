#!/usr/bin/env python3

### Advent of Code - 2021 - Day 8

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

# Part 1

digits = collections.defaultdict(int)
for l in input_lines:
    toks = l.rstrip().split(' ')
    ival = toks[0:10]
    oval = toks[11:]
    # print(ival,oval)
    for o in oval:
        u = len(set(o))
        if u == 2:
            digits[1] += 1
        if u == 4:
            digits[4] += 1
        if u == 3:
            digits[7] += 1
        if u == 7:
            digits[8] += 1
part1(sum(digits.values()))

# Part 2

#  0000
# 1    2
# 1    2
#  3333
# 4    5
# 4    5
#  6666
the_sum = 0
segments = dict()
for l in input_lines:
    segments = dict()
    digits = dict()
    toks = l.rstrip().split(' ')
    ival = toks[0:10]
    
    # sort the digits nu length - this lets us find the 5 segment numbers before
    # the 6 segment numbers, which helps us ensure the proper order when
    # checking for the number 6 below (because we need to have first found
    # the 5) I can probably use different set operations to avoid this, but
    # this was easiest
    ival = sorted(ival,key=lambda x: len(x))  # input digits
    oval = toks[11:]                          # output digits
    seen = set()
    # go through list to find the easy numbers 1, 4, 7, 8
    for i in ival:
        u = len(set(i))
        if u == 2: # found a '1'
            digits[1] = set(i)
            seen.add(i)
        if u == 4: # found a '4'
            digits[4] = set(i)
            seen.add(i)
        if u == 3: # found a '3'
            digits[7] = set(i)
            seen.add(i)
        if u == 7: # found a '7'
            digits[8] = set(i)
            seen.add(i)
        if u == 5: # 2, 3, 5?
            pass            
        if u == 6: # 0, 6, 9?
            pass
    # go through list again, to find the 3 and 9, using the digits we already found
    for i in ival:
        if i in seen:
            continue
        u = len(set(i))
        if u == 5: # 2, 3, 5
            # if we subtract the segments of a 7 from a 2,3,5 and only
            # have 2 segments left, then it must be a 3
            if len(set(i)-digits[7]) == 2:
                digits[3] = set(i)
                seen.add(i)
                continue
        if u == 6: # 0, 6, 9
            # if we union the segments of a 4 to a 0,6,9 and we don't
            # yet have all segments of an 8, then this must be a 9
            if len(set(i).union(digits[4])) != len(digits[8]):
                digits[9] = set(i)
                seen.add(i)
                continue
    # go through again, to find the 2, 5, and 6
    for i in ival:
        if i in seen:
            continue
        u = len(set(i))
        if u == 5: # 2, 5
            # if we subtract the union of a 3 and 4, from a possible 2 or 5,
            # and only have one segment remaining, then this must be a 2
            if len(set(i).difference(digits[3].union(digits[4]))) == 1:
                digits[2] = set(i)
                seen.add(i)
                continue
            # if we subtract the union of a 3 and 4, from a possible 2 or 5,
            # and we have no segments remaining, then this is a 5
            if len(set(i).difference(digits[3].union(digits[4]))) == 0:
                digits[5] = set(i)
                seen.add(i)
                continue
        if u == 6: # 0, 6
            # if this digit (0 or 6) is equal to an 8, minus a (4 minus a 5),
            # then this must be a 6
            if set(i) == digits[8].difference(digits[4].difference(digits[5])):
                digits[6] = set(i)
                seen.add(i)
                continue
    for i in ival:
        if i not in seen:
            # this is our last digit, it must be a 0!
            digits[0] = set(i)
            break

    # now loop over the output values and compare segments to compute
    # the actual digit and sum
    out = 0
    for o in oval:
        for k,d in digits.items():
            if set(o) == d:
                out *= 10
                out += k
    the_sum += out

part2(the_sum)
    