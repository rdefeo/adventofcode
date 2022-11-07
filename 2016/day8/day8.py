#!/usr/bin/env python3

### Advent of Code - 2016 - Day 8

import sys
import requests
import re
import math
import itertools
import functools
import os

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

sw = 50
sh = 6

#sw = 7
#sh = 3

screen = []
for h in range(sh):
    screen.append([])
    for w in range(sw):
        screen[h].append('.')

def prints(screen):
    for h in range(sh):
        print(''.join(screen[h]))
    print('')

def rect(screen,A,B):
    print(f"rect {A}, {B}")
    for b in range(B):
        for a in range(A):
            screen[b][a] = 'X'

def rotate_row(screen,A,B):
    print(f"rotate row {A} by {B}")
    B %= len(screen[A])
    screen[A] = screen[A][-B:] + screen[A][0:sw-B]

def rotate_col(screen,A,B):
    print(f"rotate col {A} by {B}")
    col = [screen[b][A] for b in range(sh)]
    #print(col)
    #print(f"col: {A}, shft: {B}")
    for y in range(sh):
        screen[y] = screen[y][:A] + list(col[(y-B)%sh]) + screen[y][A+1:]


# prints(screen)
# rect(screen,4,4)
# prints(screen)
# rotate_row(screen,2,2)
# prints(screen)
# rotate_col(screen,1,3)
# prints(screen)

p1 = 0
p2 = 0

for x in input_lines:
    m = re.match(r"rect (\d+)x(\d+)",x)
    if m:
        rect(screen,int(m.group(1)),int(m.group(2)))
    m = re.match(r"rotate row y=(\d+) by (\d+)",x)
    if m:
        rotate_row(screen,int(m.group(1)),int(m.group(2)))
    m = re.match(r"rotate column x=(\d+) by (\d+)",x)
    if m:
        rotate_col(screen,int(m.group(1)),int(m.group(2)))
    prints(screen)


for h in range(sh):
    for w in range(sw):
        if screen[h][w] == 'X':
            p1 += 1
part1(p1)

for x in input_lines:
    # m = re.match(r"(\d+)",x)
    pass

part2()

