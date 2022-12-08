#!/usr/bin/env python3

### Advent of Code - 2022 - Day 7

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

# Create a file system of Directory objects. They can contain files with sizes as
# well as other directories. Recursive methods to fetch directory sizes
class Directory():
    def __init__(self, name):
        self.name = name
        self.files = dict() # file to filesize
        self.dirs = dict() # dirname to directory obj
        self.parent = self
        self.size = 0
    def add_dir(self,newdir):
        nd = Directory(newdir)
        nd.parent = self
        self.dirs[newdir] = nd
    def add_file(self,filename,filesize):
        self.files[filename] = filesize
        self.size += filesize
    def get_size(self):
        s = self.size
        for d in self.dirs.values():
            s += d.get_size()
        return s
    def get_dir_sums(self,sums=[]):
        sums.append(self.get_size())
        for d in self.dirs.values():
            d.get_dir_sums(sums)
        return sums

# Parse the commands and build up our file system tree
fs = Directory('/')
curr = fs # current working directory, start at root
input_lines.pop(0)
while input_lines:
    tokens = input_lines.pop(0).split()
    if tokens[1] == 'ls':
        while input_lines[0][0] != '$':
            tokens = input_lines.pop(0).split()
            if tokens[0] == 'dir':
                curr.add_dir(tokens[1])
            else:
                curr.add_file(tokens[1],int(tokens[0]))
            if not input_lines:
                break
    elif len(tokens) == 3:
        if tokens[2] == '..':
            curr = curr.parent
        else:
            curr = curr.dirs[tokens[2]]
print('--------')

# Part 1
sums = fs.get_dir_sums()
print(sums)

part1(sum(s for s in sums if s <= 100_000))

# Part 2
total = 70_000_000
need = 30_000_000

freespace = total - sorted(sums)[-1]
must_delete = need - freespace
print(f'We need to delete at least {must_delete}')
# print(sorted(sums))
part2(sorted(s for s in sums if s >= must_delete)[0])