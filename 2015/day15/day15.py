#!/usr/bin/env python3

### Advent of Code - 2015 - Day 15

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

class Ingredient:
    def __init__(self, name, cap, dur, flav, tex, cal):
        self.name = name
        self.cap = cap
        self.dur = dur
        self.flav = flav
        self.tex = tex
        self.cal = cal
    def __repr__(self):
        return f"({self.name}: cap={self.cap}, dur={self.dur}, flav={self.flav}, tex={self.tex}, cal={self.cal})"

ing = []
for line in input_lines:
    tok = line.split()
    ing.append(Ingredient(tok[0][:-1], int(tok[2][:-1]), int(tok[4][:-1]), int(tok[6][:-1]), int(tok[8][:-1]), int(tok[10])))

def compute_score(a, b, c, d):
    cap = ing[0].cap*a + ing[1].cap*b + ing[2].cap*c + ing[3].cap*d
    dur = ing[0].dur*a + ing[1].dur*b + ing[2].dur*c + ing[3].dur*d
    flav = ing[0].flav*a + ing[1].flav*b + ing[2].flav*c + ing[3].flav*d
    tex = ing[0].tex*a + ing[1].tex*b + ing[2].tex*c + ing[3].tex*d
    cal = ing[0].cal*a + ing[1].cal*b + ing[2].cal*c + ing[3].cal*d
    cap = max(cap, 0)
    dur = max(dur, 0)
    flav = max(flav, 0)
    tex = max(tex, 0)
    score = cap * dur * flav * tex
    return (score, cal)

cookies = dict()
for a in range(100+1):
    for b in range(100+1-a):
        for c in range(100+1-(a+b)):
            for d in range(100+1-(a+b+c)):
                if a+b+c+d == 100:
                    score = compute_score(a, b, c, d)
                    cookies[(a,b,c,d)] = score # (score, cal)

part1(max(s for s,_ in cookies.values()))
part2(max(s for s,c in cookies.values() if c == 500))