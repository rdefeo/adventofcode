#!/usr/bin/env python3

### Advent of Code - 2020 - Day 11

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

state = input_lines
h = len(state)
w = len(state[0])
print(f"h: {h}, w: {w}")

surround = [
    (-1,-1),(-1,0),(-1,1),
    (0,-1),        (0,1),
    (1,-1), (1,0), (1,1)
    ]

def get_seat(state,r,c):
    if 0 <= r < h and 0 <= c < w:
        return state[r][c]
    return None

def line_of_sight(state,r,c,d):
    seat = state[r][c] # current seat
    while seat:
        r,c = r+d[0],c+d[1]
        seat = get_seat(state,r,c)
        yield seat

def count_full(part,state,r,c):
    if part == 1:
        return sum([get_seat(state,r+y,c+x) == '#' for y,x in surround])
    else:
        full = 0
        for d in surround:
            for seat in line_of_sight(state,r,c,d):
                if seat == '.':
                    continue
                full += seat=='#'
                break
        return full

def count_seats(state):
    return sum([r.count('#') for r in state])

def change_state(part,st):
    ns = st.copy()
    for r in range(h):
        for c in range(w):
            full = count_full(part,st,r,c)
            if st[r][c] == 'L' and full == 0:
                ns[r] = ns[r][0:c]+'#'+ns[r][c+1:]
            elif st[r][c] == '#' and full >= 3+part:
                ns[r] = ns[r][0:c]+'L'+ns[r][c+1:]        
    return ns

start_timer('part 1')
c = 0
while True:
    news = change_state(1,state)
    if news == state:
        #print(news)
        print(f"steps - {c}")
        part1(f"total seats: {count_seats(news)}")
        break
    state = news
    c += 1

stop_timer('part 1')

start_timer('part 2')
state = input_lines
c = 0
while True:
    news = change_state(2,state)
    if news == state:
        #print(news)
        print(f"steps - {c}")
        part2(f"total seats: {count_seats(news)}")
        break
    state = news
    c += 1
stop_timer('part 2')