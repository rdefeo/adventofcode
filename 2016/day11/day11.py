#!/usr/bin/env python3

### Advent of Code - 2016 - Day 11

import sys
import requests
import re
import math
import itertools
import functools
import os
from itertools import chain, combinations
from collections import Counter

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

# Create a list of sets of all objects on each floor. Each object is a tuple of
# element, object type. 
floors = []
for line in input_lines:
    floors.append(set(re.findall(r"(\w+)(?:-compatible)? (microchip|generator)",line)))
print(floors)
print('')

# Floors are valid if:
# - floor is empty
# - a floor only contains objects of one type (either microchip or generator)
# - floor contains object pairs: element microchip + element generator
def is_floor_valid(f):
    if not len(f): return True
    if len(set(obj_type for _,obj_type in f)) == 1:
        return True
    if all((element,'generator') in f for (element,obj_type) in f if obj_type == 'microchip'):
        return True
    return False

def next_states(state):
    moves, elevator, floors = state

    # consider moving any 2 or any 1 item from this floor
    possible = chain(combinations(floors[elevator],2),combinations(floors[elevator],1))

    for move in possible:
        for direction in [-1, 1]:
            next_elevator = elevator + direction
            if next_elevator < 0 or next_elevator >= len(floors):
                continue
            next_floors = floors.copy()
            next_floors[elevator] = next_floors[elevator].difference(move)
            next_floors[next_elevator] = next_floors[next_elevator].union(move)
            if is_floor_valid(next_floors[elevator]) and is_floor_valid(next_floors[next_elevator]):
                yield (moves+1, next_elevator, next_floors)

def all_on_top_floor(floors):
    return all(len(f) == 0 for f in floors[:3])

def count_floor_objects(state):
    moves, elevator, floors = state
    return elevator, tuple(tuple(Counter(obj_type for _, obj_type in floor).most_common()) for floor in floors)

def solve(floors):
    q = [ (0, 0, floors) ] # number of moves, elevator position, floors
    seen = set()
    while q:
        state = q.pop(0)
        moves, elevator, floors = state
        if all_on_top_floor(floors):
            return moves
        for next_state in next_states(state):
            key = count_floor_objects(next_state)
            if key not in seen:
                seen.add(key)
                q.append(next_state)

part1(solve(floors))

floors[0].add(('elerium','generator'))
floors[0].add(('elerium','microchip'))
floors[0].add(('dilithium','generator'))
floors[0].add(('dilithium','microchip'))

part2(solve(floors))
