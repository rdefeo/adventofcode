#!/usr/bin/env python3

### Advent of Code - 2020 - Day 4

import sys
import requests
import re
import math
import itertools
import functools
import os

sys.path.append('../../python/')
from aoc_utils import *

# read input data file as one large string and as an array of lines
inputfile = 'input'
if len(sys.argv) == 2:
    inputfile = sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, length: {len(input_lines)}"+CLEAR)

#start_timer()

# ###############################
# PART 1
start_timer('part 1')

# dict of field name to regex
fields = {
    'byr':r'^(19[2-9][\d]|200[0-2])$',
    'iyr':r'^(201[0-9]|2020)$', 
    'eyr':r'^(202[0-9]|2030)$',
    'hgt':r'^((1[5-8][0-9]|19[0-3])cm|(59|6[0-9]|7[0-6])in)$', 
    'hcl':r'^#[0-9a-f]{6}$',
    'ecl':r'^(amb|blu|brn|gry|grn|hzl|oth)$', 
    'pid':r'^(\d{9})$'
    }

# A passport is valid if it contains at least all 7 fields in (fields)
# for part 1, we don't care about the field values
def valid_fields(p):
    return all([k in p for k in fields])

# A passport is valid if each field matches the regex
def valid_values(p):
    return all([re.match(v,p[k]) != None for k,v in fields.items()])

# parse the input file
valid1 = 0
valid2 = 0
for line in input.replace(" ","\n").split("\n\n"):
    new_pp = dict()
    for k,v in [f.split(':') for f in line.split("\n") if f != '']:
        new_pp.update({k:v})
    valid1 += valid_fields(new_pp)
    valid2 += valid_fields(new_pp) and valid_values(new_pp)

# check for valid passports
part1(valid1)

stop_timer('part 1')

# ###############################
# PART 2
start_timer('part 2')

part2(valid2)

stop_timer('part 2')

#stop_timer()