#!/usr/bin/env python3

### Advent of Code - 2016 - Day 14

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import hashlib

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

salt = 'yjdafjpo' # sample 'abc'
index = 0

hashes = dict()
def hash_it(salt,index,part1=True):
    if part1:
        return hashlib.md5((salt+str(index)).encode()).hexdigest()
    else:
        k = hashlib.md5((salt+str(index)).encode()).hexdigest()
        # print(k)
        for _ in range(2016):
            k = hashlib.md5(k.encode()).hexdigest()
        return k

part_1 = True
index = 0
gkeys = []
while len(gkeys) < 64:
    key = hash_it(salt,index,part_1)
    # print(key)
    m = re.search(r"(.)\1\1",key)
    if m:
        # print("Found triple in",hashk,key)
        goodkey = False
        regex = re.compile("("+m.group(1)+")"+r"\1\1\1\1")
        for i in range(index+1,index+1+1000+1):
            k = hash_it(salt,i,part_1)
            if regex.search(k):
                goodkey = True
                break
        if goodkey:
            print("Adding ",i,index,key)
            gkeys.append(index)
    index += 1
part1(gkeys[-1])



# Part 2
# precompute a list of 1000 hashes
part_1 = False
index = 0
gkeys = []
hashes = [hash_it(salt,i,part_1) for i in range(1001)]
while len(gkeys) < 64:
    h = hashes.pop(0)
    m = re.search(r"(.)\1\1",h)
    if m:
        r5 = re.compile("("+m.group(1)+")"+r"\1\1\1\1")
        for k in hashes:
            if r5.search(k):
                print("Adding",index,k)
                gkeys.append(index)
    index += 1
    hashes.append(hash_it(salt,index+len(hashes),part_1))

part2(gkeys[:64][-1])