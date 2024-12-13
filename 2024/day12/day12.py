#!/usr/bin/env python3

### Advent of Code - 2024 - Day 12

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

# Helps us determine if (x,y) is valid
gardens = dict()
for y, row in enumerate(input_lines):
    for x, p in enumerate(row):
        gardens[(x,y)] = p

# Find all plots, using a flood fill method
seen = set()
fence1, fence2 = 0, 0
for y, row in enumerate(input_lines):
    for x, p in enumerate(row):
        if (x,y) not in seen:
            plot = set()
            queue = [(x,y)]
            while queue:
                cx,cy = queue.pop(0)
                if (cx,cy) in plot or (cx,cy) in seen:
                    continue
                plot.add((cx,cy))
                seen.add((cx,cy))
                for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
                    n = (cx+dx,cy+dy)
                    if n in seen or n in plot: 
                        continue
                    if n in gardens and gardens[n] == p:
                        queue.append(n)

            area = len(plot)

            # For each flooded plot found, calc the Part 1/2 fences

            # Part 1 calc:
            # every square has a perimeter of 4, minus 1 for each plot of same type that borders it
            perm = 0
            for px,py in plot:
                perm += 4
                for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
                    ax,ay = px+dx,py+dy
                    if (ax,ay) in plot:
                        perm -= 1
            # print(f"{p}: {area=} x {perm=} = {area*perm}")
            fence1 += area * perm
          
            # Part 2 calc:
            # Every continuous run of an edge in a plot is a side, in each direction
            # Holy hell - there has to be a simpler way
            xs = [x for x,_ in plot]
            ys = [y for _,y in plot]

            min_x, min_y = min(xs), min(ys)
            max_x, max_y = max(xs), max(ys)

            # find top sides
            top_sides = 0
            for r in range(min_y,max_y+1):
                c = min_x
                found_side = False
                while c <= max_x:
                    while not found_side and c <= max_x:
                        if (c,r) not in plot:
                            found_side = False
                            c += 1
                            continue
                        if (c,r-1) not in gardens or gardens[(c,r-1)] != p:
                            found_side = True
                        c += 1
                    if found_side:
                        top_sides += 1
                    while found_side and c <= max_x and (c,r) in plot:
                        if (c,r-1) not in gardens or gardens[(c,r-1)] != p:
                            c += 1
                        else:
                            found_side = False
                    found_side = False                            
                    c += 1
            # print(f"{top_sides=}")
            # find bottom sides
            bot_sides = 0
            for r in range(min_y,max_y+1):
                c = min_x
                found_side = False
                while c <= max_x:
                    while not found_side and c <= max_x:
                        if (c,r) not in plot:
                            found_side = False
                            c += 1
                            continue
                        if (c,r+1) not in gardens or gardens[(c,r+1)] != p:
                            found_side = True
                        c += 1
                    if found_side:
                        bot_sides += 1
                    while found_side and c <= max_x and (c,r) in plot:
                        if (c,r+1) not in gardens or gardens[(c,r+1)] != p:
                            c += 1
                        else:
                            found_side = False
                    found_side = False                        
                    c += 1
            # print(f"{bot_sides=}")
            # # find left sides
            left_sides = 0
            for c in range(min_x,max_x+1):
                r = min_y
                found_side = False
                while r <= max_y:
                    while not found_side and r <= max_y:
                        if (c,r) not in plot:
                            found_side = False
                            r += 1
                            continue
                        if (c-1,r) not in gardens or gardens[(c-1,r)] != p:
                            found_side = True
                        r += 1
                    if found_side:
                        left_sides += 1
                    while found_side and r <= max_y and (c,r) in plot:
                        if (c-1,r) not in gardens or gardens[(c-1,r)] != p:
                            r += 1
                        else:
                            found_side = False
                    found_side = False
                    r += 1
            # print(f"{left_sides=}")
            # find right sides
            right_sides = 0
            for c in range(min_x,max_x+1):
                r = min_y
                found_side = False
                while r <= max_y:
                    while not found_side and r <= max_y:
                        if (c,r) not in plot:
                            found_side = False
                            r += 1
                            continue
                        if (c+1,r) not in gardens or gardens[(c+1,r)] != p:
                            found_side = True
                            break
                        r += 1
                    if found_side:
                        right_sides += 1
                    while found_side and r <= max_y and (c,r) in plot:
                        if (c+1,r) not in gardens or gardens[(c+1,r)] != p:
                            r += 1
                        else:
                            found_side = False
                    found_side = False
                    r += 1
            # print(f"{right_sides=}")
            sides = top_sides + bot_sides + left_sides + right_sides
            # print(f"{p}: {area=} x {sides=} = {area*sides}")
            fence2 += area * sides

            # Just computing the top and bottom sides, then doubling also works!
            # fence2 += area * (top_sides+bot_sides) * 2

part1(fence1)
part2(fence2)
