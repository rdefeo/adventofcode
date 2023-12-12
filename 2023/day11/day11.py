#!/usr/bin/env python3

### Advent of Code - 2023 - Day 11

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

# Determine the all of the blank rows and columns, as a list of indices
blank_rows = []
blank_cols = []
for y, line in enumerate(input_lines):
    if all(g == '.' for g in line):
        blank_rows.append(y)
for x in range(len(input_lines[0])):
    if all(line[x] == '.' for line in input_lines):
        blank_cols.append(x)

# Find all galaxies in our input and assign (x,y)
gal = []
for y, line in enumerate(input_lines):
    for x, g in enumerate(line):
        if g == '#':
            gal.append((x,y))

def expand(gal, exp_const):
    """ Given a list of galaxy coords and an expansion constant, recompute
    the coords based on how many blank columns or rows came before each coord """
    ngal = []
    for g in gal:
        prev_bc = sum(bc < g[0] for bc in blank_cols)
        prev_br = sum(br < g[1] for br in blank_rows)
        ng = (g[0]-prev_bc + prev_bc*exp_const, g[1]-prev_br + prev_br*exp_const)
        ngal.append(ng)
    return ngal

def calc_dist(gal):
    """ For our list of galaxy coordinates, compute the distance between each unique pair """
    dist = 0
    for i1 in range(len(gal)):
        for i2 in range(i1+1,len(gal)):
            g1 = gal[i1]
            g2 = gal[i2]
            dist += abs(g1[0]-g2[0]) + abs(g1[1]-g2[1])
    return dist

part1(calc_dist(expand(gal, 2)))
part2(calc_dist(expand(gal, 1_000_000)))