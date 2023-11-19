#!/usr/bin/env python3

### Advent of Code - 2015 - Day 14

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

class Deer:
    def __init__(self, name, v, vt, rt):
        self.name = name
        self.v = v # velocity
        self.vt = vt # flying time
        self.rt = rt # rest time
        self.d = 0 # distance
        self.flying = True
        self.t_rem = vt # time remaining, whether flying or resting
        self.points = 0

    def compute_dist_at_time(self, time):
        """ Compute the total distance this deer can traver in 'time' sec """
        dist = 0
        t = 0
        while t <= time:
            if t + self.vt <= time:
                dist += self.v * self.vt
            else:
                dist += self.v * ((t + self.vt) - time)
            t += self.vt
            t += self.rt
        return dist

deer = dict()
for line in input_lines:
    tok = line.split()
    name, v, vt, rt = tok[0], int(tok[3]), int(tok[6]), int(tok[-2])
    deer[name] = Deer(name, v, vt, rt)

# Part 1
# Compute the max dist for each deer, return max
race_time = 2503
max_dist = 0
for d in deer:
    dist = deer[d].compute_dist_at_time(race_time)
    max_dist = max(max_dist, dist)
part1(max_dist)

# Part 2
# This time, progress every second, and compute max distance for each deer
# then award points
for t in range(race_time):
    for n, d in deer.items():
        if d.flying:
            d.d += d.v
        d.t_rem -= 1
        if d.t_rem == 0:
            d.flying = not d.flying
            if d.flying:
                d.t_rem = d.vt
            else:
                d.t_rem = d.rt
    max_dist = 0
    for d in deer.values():
        max_dist = max(max_dist, d.d)
    for n, d in deer.items():
        if d.d == max_dist:
            deer[n].points += 1
    t += 1

part2(max(deer[d].points for d in deer))
