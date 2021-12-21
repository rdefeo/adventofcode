#!/usr/bin/env python3

### Advent of Code - 2021 - Day 21

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

# Part 1
def take_turns_p1(p1,p2):
    s1, s2 = 0, 0
    rolls = 0
    die = 1
    while True:
        d = []
        for _ in range(3):
            p1 = p1 + die
            while p1 > 10: p1 -= 10
            d.append(die)
            die += 1
            if die > 100: die = 1
        s1 += p1
        rolls += 3
        # print(f"Player 1 rolls {d} and moves to space {p1} for a total score of {s1}")
        if s1 >= 1000: break
        d = []
        for _ in range(3):
            p2 = p2 + die
            while p2 > 10: p2 -= 10
            d.append(die)
            die += 1
            if die > 100: die = 1
        s2 += p2
        rolls += 3
        # print(f"Player 2 rolls {d} and moves to space {p2} for a total score of {s2}")
        if s2 >= 1000: break
    return rolls,s1,s2

# test input
rolls,s1,s2 = take_turns_p1(4,8)
print(rolls * min(s1,s2))

# real input
rolls,s1,s2 = take_turns_p1(9,10)
part1(rolls * min(s1,s2))

# Part2

# 27 dice combinations, all universe copies that have d1+d2+d3
# with the same sum will have the same outcomes
all_3die = collections.Counter([d1+d2+d3 for d1 in (1,2,3) for d2 in (1,2,3) for d3 in (1,2,3)])

univ_seen = dict()
def take_turns_p2(p1,s1,p2,s2,player=1):
    global univ_seen
    # again, most universes will have repeated states - use a cache
    if (p1,s1,p2,s2,player) in univ_seen:
        return univ_seen[(p1,s1,p2,s2,player)]
    p1_wins, p2_wins = 0, 0
    for d,cnt in all_3die.items():
        if player == 1:
            np1 = p1 + d
            if np1 > 10: np1 -= 10
            ns1 = s1 + np1
            if ns1 >= 21:
                # p1 won in this universe - which occurs cnt times
                p1_wins += cnt
            else:
                # p1 hasn't yet won, keep taking turns
                np1_wins, np2_wins = take_turns_p2(np1,ns1,p2,s2,2)
                # however many wins p1 and p2 made in the recursive call above
                # need to be scaled for all cnt universes
                p1_wins += np1_wins * cnt
                p2_wins += np2_wins * cnt
        else:
            np2 = p2 + d
            if np2 > 10: np2 -= 10
            ns2 = s2 + np2
            if ns2 >= 21:
                p2_wins += cnt
            else:
                np1_wins, np2_wins = take_turns_p2(p1,s1,np2,ns2,1)
                p1_wins += np1_wins * cnt
                p2_wins += np2_wins * cnt
    univ_seen[(p1,s1,p2,s2,player)] = (p1_wins,p2_wins)
    return p1_wins, p2_wins

# test input
print(max(take_turns_p2(4,0,8,0)))

# real input
part2(max(take_turns_p2(9,0,10,0)))