#!/usr/bin/env python3

### Advent of Code - 2018 - Day 8

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
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
input = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in input.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

sample = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'

class Node:
    def __init__(self):
        self.nodes = []
        self.meta = []
    def add_child(self,node):
        self.nodes.append(node)
    def add_meta(self,meta):
        self.meta.extend(meta)
    def __repr__(self):
        return f"c:{len(self.nodes)} m:{self.meta}"

nums = list(map(int,input.split(' ')))


def create_nodes(parent,i,nums):
    child_num = nums[i]
    meta_num = nums[i+1]
    i += 2
    for c in range(child_num):
        child = Node()
        parent.add_child(child)
        i = create_nodes(child,i,nums)
    parent.add_meta(nums[i:i+meta_num])
    return i + meta_num

nums = list(map(int,sample.split(' ')))

print(nums)
root = Node()
i = 0
create_nodes(root,0,nums)

def sum_meta(node):
    meta = 0
    for c in node.nodes:
        meta += sum_meta(c)
    meta += sum(node.meta)
    return meta

part1(sum_meta(root))

def value(node):
    if not node.nodes:
        return sum(node.meta)
    total = 0
    for m in node.meta:
        if m == 0:
            continue
        if m-1 < len(node.nodes):
            total += value(node.nodes[m-1])
    return total

part2(value(root))