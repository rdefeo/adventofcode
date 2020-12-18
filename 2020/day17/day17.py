#!/usr/bin/env python3

### Advent of Code - 2020 - Day 17

import sys
import requests
import re
import math
import itertools
import functools
import os
import collections
from functools import lru_cache
import copy

sys.path.append('../../python/')
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
#input_nums = list(map(int,input_lines))
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

# A modified 3D/4D Conway's Game Of Life


state = collections.defaultdict(lambda:'.')
def init_state():
    global state
    state.clear()
    # initialize state to input
    for y,line in enumerate(input_lines):
        for x,c in enumerate(line):
            #if c == '#':
            state[(x,y,0,0)] = c
    print(state)

def print_state(st):
    x_min, x_max = 0, 0
    y_min, y_max = 0, 0
    z_min, z_max = 0, 0
    w_min, w_max = 0, 0
    for p in st:
        x_min = min(x_min,p[0])
        y_min = min(y_min,p[1])
        z_min = min(z_min,p[2])
        w_min = min(w_min,p[3])
        x_max = max(x_max,p[0])
        y_max = max(y_max,p[1])
        z_max = max(z_max,p[2])
        w_max = max(w_max,p[3])
    for w in range(w_min,w_max+1):
        for z in range(z_min,z_max+1):
            print(f"z = {z}, w = {w}")
            for y in range(y_min,y_max+1):
                for x in range(x_min,x_max+1):
                    print(st[(x,y,z,w)],end='')
                print('')
            print('')

# one side affect of counting all active stars is that we also record
# positions that aren't in our current state - this means they're just
# 1 'unit' beyond our current state. return them, too
def count_active(part,st,p):
    a = 0
    newp = []
    r = [-1,0,1]
    for dx in r:
        for dy in r:
            for dz in r:
                if part == 1:
                    if dz == dy == dx == 0: continue
                    np = (p[0]+dx,p[1]+dy,p[2]+dz,p[3])
                    if np not in st:
                        #print(f"pos {np} not in current state")
                        newp.append(np)
                    elif st[np] == '#':
                        a += 1
                else:
                    for dw in r:
                        if dw == dz == dy == dx == 0: continue
                        np = (p[0]+dx,p[1]+dy,p[2]+dz,p[3]+dw)
                        if np not in st:
                            #print(f"pos {np} not in current state")
                            newp.append(np)
                        elif st[np] == '#':
                            a += 1
    return a,newp

# For every position in the current state, count how many
# active cubes we find, and then apply the rules
# Also, keep track of positions we're checking that aren't
# in our state and then add them as inactive, but only if
# they're inactive and have no neighbors - helps with runtime
def change_state(part,st):
    ns = copy.deepcopy(st)
    newp = []
    for p in st:
        active,np = count_active(part,st,p)
        #print(f"position {p} has {active} active cubes")
        if st[p] == '#' and active not in [2,3]:
            ns[p] = '.'
        if st[p] == '.' and active == 3:
            ns[p] = '#'
        if st[p] == '.' and active != 0:
            newp = newp + np
    #print(f"adding {len(newp)} positions")
    for n in newp:
        ns[n] = '.'
    return ns

# Perform a state change for every number of cycles. First
# initialize the state to the input, and then use the count_active
# method to find all positions, that are not in our state, but are
# on the 'outer edge' (and thus empty). Some of those positions
# might become active during our first cycle, which is why we
# prime them.
def simulate(part,state,cycles):
    init_state()
    #print_state(state)
    
    # Prime the positions on the outer edge
    newp = []
    for p in state:
        _,np = count_active(part,state,p)
        newp = newp + np
    for n in newp:
        state[n] = '.'

    # Change our state for (cycles)
    for c in range(cycles):
        nst = change_state(part,state)
        print(f"cycle {c+1}: ",end='')
        eval(f"part{part}")(sum([v=='#' for v in nst.values()]))
        state = copy.deepcopy(nst)
        #print_state(state)
    eval(f"part{part}")(sum([v=='#' for v in state.values()]))

simulate(1,state,6)

simulate(2,state,6)




