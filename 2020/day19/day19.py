#!/usr/bin/env python3

### Advent of Code - 2020 - Day 19

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

sections = input.split('\n\n')
rules = sections[0].split('\n')
messages = sections[1].split('\n')

RULES = collections.defaultdict(list)
# rule: 34: 23 13 | 55
for x in rules:
    r,rdef = x.split(': ')
    RULES[r] = rdef.replace('"','').split()
# RULE['34'] = ['23','13','|','55']
#print(RULES)

# For each rule, convert them to a regex. Since rules reference other
# rules, we need to keep iterating over all RULES until we've finally
# resolved enough rules to fully resolve Rule '0'.
def solve_zero():
    parsed_rules = {'|':'|'} # pipe is a rule which resolves to itself!
    while '0' not in parsed_rules:
        for num,sub_rules in RULES.items():
            if len(sub_rules) == 1 and sub_rules[0] in ['a','b']:
                parsed_rules[num] = sub_rules[0]
            else:
                # check if all of our sub_rules have been parsed
                if all(s in parsed_rules for s in sub_rules):
                    # now we can build our regex
                    parsed = ''.join(parsed_rules[s] for s in sub_rules)
                    parsed_rules[num] = '('+parsed+')'
    return parsed_rules['0']

# Part 1
zero_regex = re.compile('^'+solve_zero()+'$')
part1(sum(1 for msg in messages if zero_regex.match(msg)))

# Part 2: Rule rewrite

# We're told to change:
#   R8  from '42' ==> '42 | 42 8'
#   R11 from '42 31' ==> '42 31 | 42 11 31'
#
# Since the rule rewrite has the ability to loop, let's pre-expand
# the loops. R8 can be one '42', or it can be '42' followed by
# another R8, which can be one '42', or..., etc. Therefore, let's
# create multiple alternative rule definitions for R8:
#   42 | 42 42 | 42 42 42 | 42 42 42 42 | 42 42 42 42 42 |...
# And R11 becomes:
#   42 31 | 42 42 31 31 | 42 42 42 31 31 31 | 42 42 42 42 31 31 31 31 |...

# RULES['8'] = ['42','|','42','8']
# RULES['11'] = ['42','31','|','42','11','31']
RULES['8'] = ['42']
for i in range(2,10): # expanding it to 10 seemed like enough
    RULES['8'] += ['|'] + ['42']*i

RULES['11'] = ['42', '31']
for i in range(2,10):
    RULES['11'] += ['|'] + ['42']*i + ['31']*i

zero_regex = re.compile('^'+solve_zero()+'$')
part2(sum(1 for msg in messages if zero_regex.match(msg)))