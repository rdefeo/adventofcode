#!/usr/bin/env python3

### Advent of Code - 2022 - Day 19

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

blueprints = []
for bp in input_lines:
    blueprints.append(list(map(int,re.findall(r'\d+',bp))))
print(blueprints)

def create_max_geodes(bp, time):
    print(f"*** Checking blueprint {bp[0]} ***")
    seen = set()
    max_g = 0
    # time, ore robots, clay robots, obsidian robots, geode robots,
    #   num_ore, num_clay, num_obs, num_geo
    q = [ (time, 1, 0, 0, 0, 0, 0, 0, 0) ]
    # Optimization 1:
    # Determine the max number of robots we'd need to create ANY of the robots
    # during a turn. If we have X ore robots, we're generating that many ores
    # each minute! Therefore, if we'd need at most Y ores for any of the robots,
    # we can stop creating ore robots once we have Y of them. These are used
    # when determining if we can/should build a new robot.
    max_ore = max(bp[1],bp[2],bp[3],bp[5])
    max_clay = bp[4]
    max_obs = bp[6]
    while q:
        # if len(q) % 10000 == 0:
        #     print(f"qlen: {len(q)}")
        s = q.pop(0)
        if s in seen: continue
        seen.add(s)
        t, ore, clay, obs, geo, nore, nclay, nobs, ngeo = s
        # Optimization 2:
        # Keep track of the max geodes we've seen so far
        max_g = max(max_g,ngeo)
        # If the current state has too few geodes compared to the max, we'll never catch up, bail
        if ngeo < max_g-2:
            continue
        if t <= 0:
            continue
        t -= 1
        # Create new states, attempting to build a robot. Only build
        # geode robots if we can, or obsidian if we can.
        if nore >= bp[5] and nobs >= bp[6]: # buy geode
            q.append((t, ore, clay, obs, geo+1, nore-bp[5]+ore, nclay+clay, nobs-bp[6]+obs, ngeo+geo))
            continue
        if nore >= bp[3] and nclay >= bp[4] and obs < max_obs: # buy obsidian, if necessary
            q.append((t, ore, clay, obs+1, geo, nore-bp[3]+ore, nclay-bp[4]+clay, nobs+obs, ngeo+geo))
            continue
        if nore >= bp[2] and clay < max_clay: # buy clay, if necessary
            q.append((t, ore, clay+1, obs, geo, nore-bp[2]+ore, nclay+clay, nobs+obs, ngeo+geo))
        if nore >= bp[1] and ore < max_ore: # buy ore, if necessary
            q.append((t, ore+1, clay, obs, geo, nore-bp[1]+ore, nclay+clay, nobs+obs, ngeo+geo))
        q.append((t, ore, clay, obs, geo, nore+ore, nclay+clay, nobs+obs, ngeo+geo))
    return max_g

start_timer(1)
bpg = [create_max_geodes(bp,24) for bp in blueprints]
print(bpg)
part1(sum([(id+1)*g for id,g in enumerate(bpg)]))
stop_timer(1)

start_timer(2)
bpg = [create_max_geodes(bp,32) for bp in blueprints[:3]]
print(bpg)
part2(bpg[0]*bpg[1]*bpg[2])
stop_timer(2)