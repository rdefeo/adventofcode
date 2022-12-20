#!/usr/bin/env python3

### Advent of Code - 2022 - Day 17

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


H = [[0,0], [1,0], [2,0], [3,0]]
P = [[0,1], [1,0], [1,1], [1,2], [2,1]]
L = [[0,0], [1,0], [2,0], [2,1], [2,2]]
V = [[0,0], [0,1], [0,2], [0,3]]
B = [[0,0], [0,1], [1,0], [1,1]]
ROCKS = [H, P, L, V, B]

def spawn_rock(rock_index, height):
    return [[n[0]+2,n[1]+height] for n in ROCKS[rock_index].copy()]
def rock_right(rock):
    return [[n[0]+1,n[1]] for n in rock]
def rock_left(rock):
    return [[n[0]-1,n[1]] for n in rock]
def rock_down(rock):
    return [[n[0],n[1]-1] for n in rock]
rock_move = { '<': rock_left, '>': rock_right }

def print_shaft(r = None):
    max_y = max(y for _,y in shaft)
    for y in range(max_y,-1,-1):
        for x in range(0,7):
            if r and [x,y] in r:
                print('@',end='')
            else:
                print(shaft[(x,y)],end='')
        print()
    print('-------')

shaft = collections.defaultdict(lambda:'.')

def can_rock_be_here(rock):
    if any(n[0] >= 7 or n[0] < 0 for n in rock):
        return False
    if any(shaft[tuple(n)] != '.' for n in rock):
        return False
    if any(n[1] < 0 for n in rock):
        return False
    return True

gas = 0
num_rocks = 4000 # upper bound of rocks we need to drop
rock = 0 # which rock are we moving?
highest_rock = 0 # no rocks at start, so our floor is the highest
heights = [] # keep track of all delta in height

for r in range(num_rocks):
    prev_highest = highest_rock

    R = spawn_rock(rock, highest_rock + 3)

    done_falling = False
    while not done_falling:
        # try moving rock in gas direction
        nr = rock_move[finput[gas]](R)
        gas = (gas+1) % len(finput) # get the next gas, looping if necessary

        if can_rock_be_here(nr):
            R = nr

        # make rock fall
        rd = rock_down(R)
        if can_rock_be_here(rd):
            R = rd
        else:
            done_falling = True
    
    # rock is done falling, affix it in shaft
    for n in R:
        shaft[tuple(n)] = '#'
    
    highest_rock = max(y for x,y in shaft if shaft[(x,y)] == '#') + 1
    heights.append(highest_rock - prev_highest)

    rock = (rock + 1) % 5 # move to next rock, looping if necessary

    # Part 1
    if r+1 == 2022:
        part1(highest_rock)
  
# Part 2
# Given the change in height after every dropped rock, find the pattern
def find_pattern():
    for h in range(len(heights)):
        p = heights[h:]
        for r in range(2, len(p)//2):
            if p[:r] == p[r:2*r]:
                if all([(p[:r] == p[y:y+r]) for y in range(r,len(p)-r,r)]):
                    return heights[:h], heights[h:h+r]
beginning, pattern = find_pattern()
# print(beginning, pattern)

# Since heights are all deltas, summing them gives the overall height. We first
# sum the beginning, non-repeating portion. Then, we add the height of the pattern
# as many times as will fit before we hit the total rock count. Lastly, we add
# the portion of the pattern that remains.
p2_rocks = 1000000000000
b_len = len(beginning)
p_len = len(pattern)
part2(sum(beginning) + sum(pattern) * ((p2_rocks-b_len) // p_len) \
    + sum(pattern[:((p2_rocks-b_len) % p_len)]))
