#!/usr/bin/env python3

### Advent of Code - 2019 - Day 8

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

# Given our input image size
W = 25
H = 6
layers = collections.defaultdict(list)
for i,p in enumerate(finput):
    layers[i // (W*H)].append(p)

# Part 1
# Count the number of zeroes per layer. Then, for the layer with the
# least zeroes, multiply the number of 1s and 2s
zeroes = {l:collections.Counter(layers[l])['0'] for l in layers}
minz = collections.Counter(layers[min(zeroes,key=zeroes.get)])
part1(minz['1']*minz['2'])

# Part 2
# Flatten the layers
final = layers[len(layers)-1] # start at bottom layer
for l in range(len(layers)-2,-1,-1):
    for i,p in enumerate(layers[l]):
        if p != '2':
            final[i] = p
# Print the resulting flattened image
for h in range(H):
    for w in range(W):
        print('#',end='') if final[h*W+w] == '1' else print(' ',end='')
    print('')

