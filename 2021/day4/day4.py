#!/usr/bin/env python3

### Advent of Code - 2021 - Day 4

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

draw, *boards = finput.split('\n\n')

draw = draw.split(',')
boards = [b.split() for b in boards]

def print_board(m):
    for y in range(5):
        for x in range(5):
            print(f"{m[y*5+x]:3}",end='')
        print('')
    print('')

def winner(b):
    # check for horizontal winner
    for i in range(0,25,5):
        if all(x == 'X' for x in b[i:i+5]):
            return True
    # now vertical
    for i in range(0,5):
        if all(x == 'X' for x in b[i:25:5]):
            return True
    return False

p1 = None
winners = set()
for d in draw:
    for i,b in enumerate(boards):
        if d in b:
            # if this drawn number is in the board, get it's index and mark the location
            ind = b.index(d)
            boards[i][ind] = 'X'
            if i not in winners and winner(b):
                # if this board hasn't won yet, and is now a winner,
                s = sum(int(b[i]) for i,v in enumerate(b) if v != 'X') * int(d)
                if not p1: # remember our first winner for Part 1...
                    p1 = s
                winners.add(i) # remember that this board just won
                if len(winners) == len(boards):
                    # we found our last winner!
                    part1(p1)
                    part2(s)
                    exit()


