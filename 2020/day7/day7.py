#!/usr/bin/env python3

### Advent of Code - 2020 - Day 7

import sys
import requests
import re
import math
import itertools
import functools
import os

sys.path.append('../../python/')
from aoc_utils import *

from collections import defaultdict

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


bag_parents = defaultdict(list)
bag_contents = defaultdict(list)
for x in input_lines:
    parent,contents = x.split("s contain ")
    if contents == 'no other bags.':
        continue
    inner_bags = re.findall(r"(\d+) (\w+ \w+ bag)s?[,.]",contents)
    bag_contents[parent] = inner_bags
    for num,color in inner_bags:
        bag_parents[color].append(parent)

bags = ['shiny gold bag']
parents = set()
while bags:
    color = bags.pop(0)
    for parent in bag_parents[color]:
        parents.add(parent)
        bags.append(parent)

#print(parents)
part1(len(parents))

def count_inner_bags(bag):
    contents = bag_contents[bag]
    return 1 + sum([int(n)*count_inner_bags(b) for (n,b) in contents])

part2(count_inner_bags('shiny gold bag')-1)
