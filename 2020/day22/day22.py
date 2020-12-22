#!/usr/bin/env python3

### Advent of Code - 2020 - Day 22

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
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)


p1,p2 = input.split('\n\n')

player1 = list(map(int,p1.split('\n')[1:]))
player2 = list(map(int,p2.split('\n')[1:]))

def score(hand):
    return sum((len(hand)-i)*c for i,c in enumerate(hand))

print("Part 1")
while player1 and player2:
    p1 = player1.pop(0)
    p2 = player2.pop(0)
    if p1 > p2:
        player1.append(p1)
        player1.append(p2)
    else:
        player2.append(p2)
        player2.append(p1)
print('player 1',score(player1))
print('player 2',score(player2))

print("Part 2")
p1,p2 = input.split('\n\n')
player1 = list(map(int,p1.split('\n')[1:]))
player2 = list(map(int,p2.split('\n')[1:]))

def play_game(pl1,pl2):
    seen = set()
    while pl1 and pl2:
        # if we've seen pl1 and pl2 in this game before - pl1 always wins
        handkey = (tuple(pl1),tuple(pl2))
        if handkey in seen:
            return 1, pl1
        seen.add(handkey)
        card1 = pl1.pop(0)
        card2 = pl2.pop(0)
        
        # do we need a sub-game?
        if card1 <= len(pl1) and card2 <= len(pl2):
            spl1 = pl1[:card1]
            spl2 = pl2[:card2]
            winner, _ = play_game(spl1,spl2)
        else:
            # winner is 1 or 2, convert False,True to the right value
            winner = (card2 > card1) + 1
        if winner == 1:
            pl1.append(card1)
            pl1.append(card2)
        else:
            pl2.append(card2)
            pl2.append(card1)
    return winner, pl1 if winner == 1 else pl2

winner, whand = play_game(player1,player2)
print('winning player: ',winner)
print('final',score(whand))
