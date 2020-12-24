#!/usr/bin/env python3

### Advent of Code - 2018 - Day 5

import sys
import requests
import re
import math
import itertools
import functools
import os
import collections
from functools import lru_cache
import string

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

def can_react(a : str,b : str):
    if a.upper() != b.upper():
        return False
    if ord(a) == ord(b):
        return False
    return True

polymer = input
# polymer = 'aA'
# polymer = 'abBA'
# polymer = 'abAB'
# polymer = 'aabAAB'
# polymer = 'dabAcCaCBAcCcaDA'

# reaction = True
# while reaction:
#     # print(polymer)
#     newp = ''
#     i = 0
#     reaction = False
#     while i < len(polymer)-1:
#         if can_react(polymer[i],polymer[i+1]):
#             i += 2
#             reaction = True
#             continue
#         else:
#             newp += polymer[i]
#             i += 1
#     if i == len(polymer)-1:
#         newp += polymer[-1]
#     polymer = newp
# print(polymer)
# part1(len(polymer))


def react(pol):
    reaction = True
    while reaction:
        # print(pol)
        newp = ''
        i = 0
        reaction = False
        while i < len(pol)-1:
            if can_react(pol[i],pol[i+1]):
                i += 2
                reaction = True
                continue
            else:
                newp += pol[i]
                i += 1
        if i == len(pol)-1:
            newp += pol[-1]
        pol = newp
    return pol

best_reaction = dict()
for u in string.ascii_lowercase:
    U = u.upper()
    newp = polymer.replace(u,'').replace(U,'')
    best_reaction[u] = len(react(newp))
print(best_reaction)
print(min(best_reaction,key=best_reaction.get))

