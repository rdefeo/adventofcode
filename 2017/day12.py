#!/usr/bin/env python3

import re
import functools
import collections
input = open('day12.txt','r').read().strip()

sample = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
"""
sample = input
programs = collections.defaultdict(list)
for p in sample.strip().split('\n'):
    pn,pl = p.split(' <-> ')
    programs[pn] = pl.split(', ')
#print(programs)

def solve(z,seen=set()):
    links = programs[z]
    for l in links:
        if l not in seen:
            seen.add(l)
            solve(l,seen)
    return seen

print("Part 1")
zlist = solve('0')
#print(zlist)
print(len(zlist))


print("Part 2")
all_pipes = set(programs.keys())
groups = 0
while all_pipes:
    curr_group_pipes = set(solve(min(all_pipes)))
    all_pipes.difference_update(curr_group_pipes)
    groups += 1
print(groups)
