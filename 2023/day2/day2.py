#!/usr/bin/env python3

### Advent of Code - 2023 - Day 2

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

games = dict()
for game in input_lines:
    id, rounds = game.split(':')
    id = int(id.split(' ')[1])
    
    games[id] = dict()
    for round in rounds.split(';'):
        for cube in round.split(','):
            amt, color = cube.strip().split(' ')
            games[id][color] = max(games[id].get(color,0), int(amt))

red = 12
green = 13
blue = 14

possible = 0
power = 0
for id, colors in games.items():
    r, g, b = colors.get('red',0), colors.get('green',0), colors.get('blue',0)
    if r <= red and g <= green and b <= blue:
        possible += id
    power += (r or 1) * (g or 1) * (b or 1)
part1(possible)
part2(power)


