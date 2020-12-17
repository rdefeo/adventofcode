#!/usr/bin/env python3

import sys
import requests
import re
import math
import itertools
import functools

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as array
inputfile = 'input'
if len(sys.argv) == 2:
    inputfile = sys.argv[1]
input = [line.rstrip() for line in open(inputfile,'r').readlines()]

#start_timer()

# ###############################
# # PART 1
start_timer('part 1')

# for every (right) and (down), check the tree grid. hit a tree? increment
# if we moved too far (right), modulo the width of the grid and continue
def count_trees(right,down):
    c = 0
    trees = 0   
    for r in range(0,len(input),down):
        c = c % len(input[r])
        if input[r][c] == '#':
            trees += 1
        c += right
    return(trees)
    
part1(count_trees(3,1))

stop_timer('part 1')

# ###############################
# PART 2
start_timer('part 2')

# Same as part 1, but do it for several (right,down) pairs
# then multiply the counts
slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]
part2(math.prod([count_trees(*s) for s in slopes]))

stop_timer('part 2')

#stop_timer()