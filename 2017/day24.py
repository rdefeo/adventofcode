#!/usr/bin/env python3

import collections
import sys

infile = 'day24.txt' if len(sys.argv)<2 else sys.argv[1]
input = open(infile,'r').read().strip().split('\n')

components = collections.defaultdict(set)

# port number to the components it appears in
# e.g. 3 -> [(2,3),(3,4),(3,5)]
for c in input:
    a,b = c.split('/')
    components[int(a)].add((int(a),int(b)))
    components[int(b)].add((int(a),int(b)))

def calc_max_strength(port_num,seen):
    max_str = 0
    for comp in components[port_num]:
        if comp not in seen:
            seen.add(comp)
            other_port = comp[1] if port_num == comp[0] else comp[0]
            strength = sum(comp) + calc_max_strength(other_port,seen)
            max_str = max(max_str,strength)
            seen.discard(comp)
    return max_str

strength = calc_max_strength(0,set())
print('Part 1:',strength)

def calc_max_len_strength(port_num,seen):
    max_len = 0
    max_str = 0
    for comp in components[port_num]:
        if comp not in seen:
            seen.add(comp)
            other_port = comp[1] if port_num == comp[0] else comp[0]
            (length,strength) = calc_max_len_strength(other_port,seen)
            length += 1
            if length >= max_len:
                max_str = sum(comp) + strength
                max_len = max(max_len,length)
            seen.discard(comp)
    return max_len, max_str

length, strength = calc_max_len_strength(0,set())
print('Part 2:',length,strength)
