#!/usr/bin/env python3

### Advent of Code - 2020 - Day 16

import sys
import requests
import re
import math
import itertools
import functools
import os
import collections
from functools import lru_cache

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as one long string and as an array of lines
inputfile = 'input'
if len(sys.argv) == 2:
    inputfile = sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)


# just checks that there's at least one field thats valid for 'f'
def get_field(f):
    for name,(a,b,c,d) in ranges.items():
        if a <= f <= b or c <= f <= d:
            return name
    return None

# returns *every* field whose range includes 'f'
def get_all_field_names(f):
    names = set()
    for name,(a,b,c,d) in ranges.items():
        if a <= f <= b or c <= f <= d:
            names.add(name)
    return names

# parse the input into each section
(sect1,sect2,sect3) = input.split('\n\n')

ranges = collections.defaultdict(list)
for x in sect1.split('\n'):
    m = re.findall(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)",x)[0]
    ranges[m[0]] = list(map(int,m[1:]))
#print(ranges)

mine = list(map(int,sect2.split('\n')[1].split(',')))
#print(mine)

nearby = list(list(map(lambda l:list(map(int,l.split(','))),sect3.split('\n')[1:])))
#print(nearby)

# Part 1
part1(sum([i for n in nearby for i in n if not get_field(i)]))

# Part 2

# for every ticket (v), if valid, get all possible field names
# (n) for each field position (i) and store into (fields)
#   fields[ position ] => set( all names seen in position )

# prime fields so that every position has all possible fields
fields = {r:ranges.keys() for r in range(len(ranges))}

for v in nearby:
    for i,f in enumerate(v):
        n = get_all_field_names(f)
        if not n: continue  # no names found for f, v is invalid
        fields[i] &= n      # start pruning fields for position i
#print(fields)

# Made the assumption that there had to be at least one position
# that only had one field name, otherwise the answer would be
# ambiguous. Therefore, find all positions that only have one 
# name and store them in (final). Also store them into (poplist)
# so that we can go back through (fields) and remove every
# occurrence of the field name, thus making other sets smaller
#
#   final[ name ] => position

final = dict()
while fields:
    poplist = []
    for i,f in fields.items():
        if len(f) == 1:
            part2(f"position {i} is {f}")
            final[min(f)] = i
            poplist.append((i,f))
    for i,p in poplist:
        del fields[i]
        for i,f in fields.items():
            fields[i] -= p      
#print(final)
#print(F"Mine: {mine}")

# calculate product
p = 1
for i,j in enumerate(mine):
    for n,f in final.items():
        if f == i and n[0:6] == 'depart':
            print(f"field {f} has value {j}")
            p *= j
            break
part2(p)
