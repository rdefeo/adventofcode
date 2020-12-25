#!/usr/bin/env python3

### Advent of Code - 2020 - Day 25

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache

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


key1 = int(input_lines[0])
key2 = int(input_lines[1])



# Transform subject number and count loops
def transform(sub):
    val = 1
    loop = 1
    while True:
        val = (val*sub)%20201227
        yield val, loop
        loop += 1

# sample inputs
# key1 = 5764801
# key2 = 17807724

print("Card/Door public keys:",key1,key2)

loop1 = loop2 = 0
# Using our transform method, and starting with '7', keep
# applying the transform until we encounter each of our
# public keys - and keep track of how many loops it took
# to get there.
for v,l in transform(7):
    if v == key1 and not loop1:
        loop1 = l
    if v == key2 and not loop2:
        loop2 = l
    if loop1 and loop2:
        break
print("Card/Door loop sizes:",loop1,loop2)

# Now we know that key1 transformed loop2 times, yields the encryption key

encryption_key = 0
for v,l in transform(key1):
    if l == loop2:
        encryption_key = v
        break
part1(encryption_key)

# Also, key2 transformed loop1 times, should produce the same
for v,l in transform(key2):
    if l == loop1:
        print(f"Verifying: {encryption_key} == {v}?: {encryption_key==v}")
        break

