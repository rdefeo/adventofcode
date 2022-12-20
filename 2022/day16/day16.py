#!/usr/bin/env python3

### Advent of Code - 2022 - Day 16

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import heapq

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


valve_graph = collections.defaultdict(set)
valve_rates = dict()
for line in input_lines:
    rate = int(re.findall(r'(\d+)',line)[0])
    v = re.findall(r'[A-Z]{2}',line)
    print(f"{v[0]} has rate {rate}, connects to {v[1:]}")
    valve_rates[v[0]] = rate
    for nv in v[1:]:
        valve_graph[v[0]].add(nv)

# Compute the shortest path between any two valves using BFS
def shortest_path(start, end):
    q = collections.deque([(start, 0)])
    seen = set()
    while q:
        valve, steps = q.popleft()
        if valve in seen: continue
        if valve == end: return steps
        seen.add(valve)
        for next_valve in valve_graph[valve]:
            q.append((next_valve,steps+1))

# These are the only valves worth caring about
non_zero_valves = [valve for valve, rate in valve_rates.items() if rate > 0]
non_zero_valves.append('AA') # can't forget about our starting position!

# Find the shortest path between all non-zero valve pairs
shortest = collections.defaultdict(dict)
for i, start in enumerate(non_zero_valves):
    for end in non_zero_valves[i+1:]:
        steps = shortest_path(start, end)
        shortest[start][end] = steps
        shortest[end][start] = steps

# Determine every path from 'AA' through every other valve, as long as time doesn't run out
# Since we're only looking at the shortest paths we created above, we're only going to visit
# valves worth opening. Compute the new pressure after opening the next valve, taking into
# account the time taken to walk there. Note that we might not get to visit *every* valve
# before time runs out! This will help us for Part 2
def traverse(time_remaining):
    paths = collections.defaultdict(lambda: -1)
    q = collections.deque([('AA', 0, time_remaining, set())])
    while q:
        valve, pressure, time_remaining, opened = q.popleft()

        paths[frozenset(opened)] = max(paths[frozenset(opened)],pressure)

        next_valves = (nv for nv in shortest[valve] if nv not in opened and shortest[valve][nv] < time_remaining)
        for nv in next_valves:
            new_time = time_remaining - shortest[valve][nv] - 1
            new_pressure = new_time * valve_rates[nv]
            new_opened = opened | { nv }
            q.append((nv, pressure+new_pressure, new_time, new_opened))
    return paths

# Part 1
# Get all of the paths we can walk over 30 minutes
paths = traverse(30)

# print(paths)
part1(max(paths.values()))

# Part 2
# Get all of the paths we can walk over 26 minutes
paths = traverse(26)
# Since not all traversed paths will open all valves, let's find the max pressure for two
# paths: one path by us, one by the elephant - as long as our paths don't overlap
max_pressure = 0
for our_path, our_pressure in paths.items():
    for ele_path, ele_pressure in paths.items():
        if not our_path & ele_path:
            max_pressure = max(max_pressure,our_pressure+ele_pressure)
part2(max_pressure)

exit()

# Fully recursive solution - this takes significantly longer for Part 2
states = collections.defaultdict(int)
def travel(valve, opened, tr, elephant):
    global states
    if tr == 0:
        if elephant > 0:
            return travel('AA',opened.copy(),26,elephant-1)
        return 0
    
    state_key = (valve,tuple(opened),tr,elephant)
    if state_key in states:
        return states[state_key]

    pressure = 0
    if valve not in opened and valve_rates[valve] > 0:
        pressure = max(pressure, 
            (tr-1)*valve_rates[valve] + travel(valve, opened | {valve}, tr-1, elephant))
    
    for v in valve_graph[valve]:
        pressure = max(pressure, travel(v, opened.copy(), tr-1, elephant))
    
    states[state_key] = pressure
    return pressure

# 1737
part1(travel('AA',set(),30,0))

# 2216
part2(travel('AA',set(),26,1))

