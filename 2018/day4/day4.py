#!/usr/bin/env python3

### Advent of Code - 2018 - Day 4

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

class Guard:
    def __init__(self,id):
        self.id = id
        self.wakes = collections.defaultdict(int)
        self.sleeping = collections.defaultdict(int)
        self.last_sleep = 0
        self.max_sleep = [0,0] # min, max sleep
    def __repr__(self):
        return f"{self.id}: sleeping:{self.sleeping}"
    def falls_asleep(self,time):
        self.last_sleep = int(time[-2:])
        #print(self.id,"last_sleep",self.last_sleep)
    def wakes_up(self,time):
        # from self.sleep to time, mark the minutes asleep
        wakes = int(time[-2:])
        for s in range(self.last_sleep,wakes):
            self.sleeping[s] += 1
            if self.sleeping[s] > self.max_sleep[1]:
                self.max_sleep = [s,self.sleeping[s]]
    def total_sleep_time(self):
        return sum(v for v in self.sleeping.values())

guards = dict()
last_guard = ''
for i,x in enumerate(sorted(input_lines)):
    #print(x)
    time,action = x.split("] ")

    if action.startswith("Guard "):
        id = int(action.split(' ')[1][1:])
        if id not in guards:
            guards[id] = Guard(id)
        last_guard = id
    elif action.startswith("falls"):
        #print('guard:',guards[last_guard].id,'falls asleep at',time)
        guards[last_guard].falls_asleep(time[1:])
    elif action.startswith("wakes"):
        guards[last_guard].wakes_up(time[1:])

#print(guards)

most_asleep = 0
max_sleep = 0
for n,g in guards.items():
    tot_sleep = g.total_sleep_time()
    if tot_sleep > max_sleep:
        most_asleep = n
        max_sleep = tot_sleep
#print(most_asleep,max_sleep)
    
sleepiest_min = sorted(guards[most_asleep].sleeping.items(),key=lambda x:x[1],reverse=True)[0]
part1(most_asleep*sleepiest_min[0])

# Part 2
# This is ugly - should figure out a better data structure
minutes = collections.defaultdict(list)
for g in guards.values():
    for m,a in g.sleeping.items():
        minutes[m].append((a,g.id))

#print(minutes)
most_per_min = collections.defaultdict(tuple)
for m,t in minutes.items():
    most_per_min[m] = max(t)
#print(most_per_min)
most = [0,(0,0)]
for m,t in most_per_min.items():
    if t[0] > most[0]:
        most = (t[0],(m,t[1]))
#print(most)
part2(most[1][0]*most[1][1])