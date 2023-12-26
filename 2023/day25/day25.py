#!/usr/bin/env python3

### Advent of Code - 2023 - Day 25

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import heapq, random

sys.path.append('../../python/')
from aoc_utils import *
import pydot

# read input data file as one long string and as an array of lines
inputfile = 'input' if len(sys.argv) < 2 else sys.argv[1]
if not os.path.exists(inputfile):
    print(RED+f"Input file {inputfile} not found!"+CLEAR)
    quit()
finput = open(inputfile,'r').read().rstrip()
input_lines = [line.strip() for line in finput.split('\n')]
print(DBLUE+f"Input <{inputfile}>, num lines: {len(input_lines)}"+CLEAR)

# Part 1
# To determine which 3 wires to cut from our graph of wires we first pick two
# random components and find the shortest path between them. For this path, 
# we keep track of a flow count to see how many times we traverse a given wire.
# If we do this again, and again, and again, some wires will get used more than
# others. The idea is that since we know all ~1400 components will be separated
# into two graphs after the cut, that the 3 wires connecting those two graphs
# will see many traversals. So we pick two random components 1000 times and
# record traversals in 'flow'. The 3 most-used wires should be the ones we cut!

# After cutting those wires (removing them from our set), we count how many disjoint
# graphs we end up with. We do this by assigning each component a 'parent' (initially
# set to itself). Then for every wire, we merge them and reassign a new parent.
# We're left with every component ultimating having one of two parents - our two graphs
# Lastly, we multiply the size of each graph for our answer

# This solution works surprisingly well and can produce the correct results with
# as few as 100 random components!

wires = set()
graph = collections.defaultdict(set)
for line in input_lines:
    comp = line.replace(':','').split()
    for c in comp[1:]:
        if (c,comp[0]) not in wires:
            wires.add((comp[0],c))
        graph[comp[0]].add(c)
        graph[c].add(comp[0])

def find_path(a,b):
    """ Classic Dijkstra to find the shortest path from a to b """
    q = [ (0, a, []) ] # path_len, node, path
    seen = set()
    path_lens = collections.defaultdict(int)
    while q:
        (plen, v1, path) = heapq.heappop(q)
        if v1 in seen: continue
        seen.add(v1)
        path = [v1] + path
        if v1 == b: return (plen, path)
        for v2 in graph[v1]:
            if v2 in seen: continue
            prev = path_lens[v2]
            next = plen + 1
            if prev == 0 or next < prev:
                path_lens[v2] = next
                heapq.heappush(q, (next, v2, path))
    return float("inf"), None

flow = collections.defaultdict(int)
wire_list = list(wires)
for _ in range(1000):
    # pick two random components
    same = True
    while same:
        rw = random.sample(range(0,len(wire_list)),k=2)
        c1 = wire_list[rw[0]][0]
        c2 = wire_list[rw[1]][0]
        if c1 != c2 and (c1,c2) not in wires and (c2,c1) not in wires:
            same = False
    # print(c1,c2)
    plen, path = find_path(c1,c2)
    # print(path)
    for c1,c2 in zip(path,path[1:]):
        if (c1,c2) in flow:
            flow[(c1,c2)] += 1
        elif (c2,c1) in flow:
            flow[(c2,c1)] += 1
        else:
            flow[(c1,c2)] = 1
# print(flow)
wires_to_cut = sorted(flow.items(),key=lambda x:x[1])[-3:]
print(wires_to_cut)

def cut(w, wires):
    """ Remove the wire from our set, no matter which way it's facing. """
    if w in wires:
        wires.discard(w)
    if (w[1],w[0]) in wires:
        wires.discard((w[1],w[0]))
    return wires

for c in wires_to_cut:
    cut(c[0],wires)

# Wires to cut for example
# cut(('hfx','pzl'),wires)
# cut(('bvb','cmg'),wires)
# cut(('nvd','jqt'),wires)

def find_disjoint(wires):
    """ Given our set of wires (graph edges), we keep merging them and defining
    new "parents". If there is only one graph (non-disjoint) then all nodes will
    merge into a single parent. The number of parents at the end will be the number
    of disjoint graphs. We also keep track of which edges (wires) are in each graph """
    parent = { a: a for a,_ in wires } | { b: b for _,b in wires }

    def find(w):
        if w != parent[w]:
            parent[w] = find(parent[w])
        return parent[w]

    def union(x,y):
        parent_x = find(x)
        parent_y = find(y)
        if parent_x != parent_y:
            parent[parent_y] = parent_x

    for x,y in wires:
        union(x,y)

    dict_pair = collections.defaultdict(list)
    for x,w in enumerate(parent):
        dict_pair[find(w)].append(x)
    return dict_pair

sets = find_disjoint(wires)
keys = list(sets.keys())
if len(keys) == 2:
    part1(len(sets[keys[0]]) * len(sets[keys[1]]))
else:
    print("no dice")

# Graphviz plot - the resulting image is so large, we can't read the wires to cut
# graph = pydot.Dot('wires',graph_type='digraph')
# wires = set()
# nodes = dict()
# for line in input_lines:
#     components = line.replace(':','').split()
#     if components[0] not in nodes:
#         nodes[components[0]] = pydot.Node(components[0])
#     comp = nodes[components[0]]
#     for c in components[1:]:
#         wires.add((components[0],c))
#         if c not in nodes:
#             nodes[c] = pydot.Node(c)
#         cnode = nodes[c]
#         graph.add_edge(pydot.Edge(comp,cnode))
#         if (c,components[0]) not in wires:
#             wires.add((c,components[0]))
# graph.write_png('wires.png')
# exit()

