#!/usr/bin/env python3

### Advent of Code - 2018 - Day 10

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
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

class Light:
    def __init__(self,pos,vel):
        self.p = pos
        self.v = vel
    def update(self):
        self.p = (self.p[0]+self.v[0],self.p[1]+self.v[1])

lights = []
for point in input_lines:
    m = list(map(int,re.findall(r"-?\d+",point)))
    lights.append(Light((m[0],m[1]),(m[2],m[3])))

def print_sky(sky):
    min_x = min([l.p[0] for l in lights])
    min_y = min([l.p[1] for l in lights])
    max_x = max([l.p[0] for l in lights])
    max_y = max([l.p[1] for l in lights])
    for y in range(min_y,max_y+1):
        for x in range(min_x,max_x+1):
            print(sky[(x,y)],end='')
        print('')

def create_sky(lights):
    sky = collections.defaultdict(lambda:'.')
    for l in lights:
        sky[l.p] = '#'
    return sky

sky = create_sky(lights)
# print("Initially")
# print_sky(sky)

min_y = min([l.p[1] for l in lights])
max_y = max([l.p[1] for l in lights])
s = 0
while max_y-min_y > 10:
    s += 1
    print(f"After {s} second")
    
    for l in lights:
        l.update()
    min_y = min([l.p[1] for l in lights])
    max_y = max([l.p[1] for l in lights])
    
    print(f"Height: {max_y-min_y}")
    if max_y-min_y > 10:
        continue
    sky = create_sky(lights)
    print_sky(sky)


