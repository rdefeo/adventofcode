#!/usr/bin/env python3

### Advent of Code - 2020 - Day 21

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

# all allergens to the unique set of foods they might be in
allergens = dict()
# how many times each ingredient has been seen across all foods
ingredient_count = collections.defaultdict(int)

for x in input_lines:
    x = x[:-1] # remove last paren
    ing,al = x.split(' (contains ')
    ings = ing.split(' ')

    al = al.split(', ')
    for a in al:
        if a not in allergens:
            allergens[a] = set(ings)
        else:
            allergens[a] &= set(ings)

    for i in ings:
        ingredient_count[i] += 1

# Part 1
print("allergens:",allergens)

# set of all ingredients listed with each allergens (a reverse of 'allergens' set)
ing_with_allergens = set(x for a in allergens.values() for x in a)
#print(ing_with_allergens)

# take the difference to find ingredients not associated with any allergens
all_ingredients = set(ingredient_count.keys()) - ing_with_allergens
#print(all_ingredients)

# sum their occurrences
part1(sum(ingredient_count[i] for i in all_ingredients))


# Part 2
# Now find the exact pairing of ingredients to allergens
# We already have the list of dangerous ingredients with their possible
# allergens in (ing_with_allergens)
# We also have a set of allergens to possible foods in (allergens)
# 
print("dangerous ingredients:",ing_with_allergens)

# For every ingredient found in (allergens), remove it if it's the only
# one listed, then remove it from all other allergen sets.
# Then repeat until we've removed them all
# (we did the same thing with boarding passes on Day 16)
   
dangerous = dict()
while allergens:
    poplist = []
    for a,ing in allergens.items():
        if len(ing) == 1:
            dangerous[min(ing)] = a
            poplist.append((a,ing))
    for a,ing in poplist:
        del allergens[a]
        for i in allergens:
            allergens[i] -= ing
print("dangerous w/ allergen:",dangerous)
# sort the dangerous food ingredients by their allergen name (by value)
part2(','.join(x[0] for x in sorted(dangerous.items(),key=lambda i:i[1])))
