#!/usr/bin/env python3

### Advent of Code - 2024 - Day 5

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

r, u = finput.split("\n\n")
r = r.split("\n")
u = u.split("\n")

# rules[x] = { y } - means x must come before y
rules = collections.defaultdict(set)
# inverted rule set
rules_inv = collections.defaultdict(set)
for rule in r:
    k,v = rule.split("|")
    rules[k].add(v)
    rules_inv[v].add(k)

def compare_pages(a,b):
    if a in rules and b in rules[a]:
        return -1
    if b in rules and a in rules[b]:
        return 1
    return 0

p1 = 0
p2 = 0
for update in u:
    pages = update.split(",")
    correct = True
    for i, p in enumerate(pages):
        for j in range(i+1,len(pages)):
            if p in rules_inv and pages[j] in rules_inv[p]:
                correct = False
                break
        if not correct:
            break
    if correct:
        # print(update)
        p1 += int(pages[len(pages)//2])
    else:
        sp = sorted(pages,key=functools.cmp_to_key(compare_pages))
        p2 += int(sp[len(sp)//2])
        
part1(p1)
part2(p2)
