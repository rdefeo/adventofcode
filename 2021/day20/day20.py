#!/usr/bin/env python3

### Advent of Code - 2021 - Day 20

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
from collections import Counter

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

enh, img_data = finput.split('\n\n')

img = collections.defaultdict(str)
img_data = img_data.split('\n')
for y in range(len(img_data)):
    for x in range(len(img_data[0])):
        img[(x,y)] = img_data[y][x]

def bounds(i):
    k = i.keys()
    min_x, max_x = min(x for x,_ in k), max(x for x,_ in k)
    min_y, max_y = min(y for _,y in k), max(y for _,y in k)
    return (min_x,max_x,min_y,max_y)

def print_img(i):
    mx,Mx,my,My = bounds(i)
    print('')
    for y in range(my,My+1):
        for x in range(mx,Mx+1):
            print(i[x,y],end='')
        print('')

def get_value(x, y, im, default_val):
    b = ''
    for j in (-1,0,1):
        for i in (-1,0,1):
            v = im.get((x+i,y+j),default_val)
            b += '1' if v == '#' else '0'
    v = int(b,2)
    return enh[v]

def enhance(im, default_val):
    mx, Mx, my, My = bounds(im)
    ni = collections.defaultdict(str)
    for y in range(my-1,My+2):
        for x in range(mx-1,Mx+2):
            ni[(x,y)] = get_value(x,y,im,default_val)
    return ni

# Part 1
# Enhancement algorithm value zero represents the newly enhanced value within
# the infinite plane. That is, 9 dark pixels (all bits zero) will select algo
# value 0. This new value can change based on the input. If value zero is '.'/dark,
# then the infinite plane remains dark for all enhancements. If it is '#'/light,
# then the infinite plane will toggle from dark to light, and then back, with 
# each enhancement. Therefore, we need to toggle the value as well so it will be
# correct when probing unknown pixels (in function get_value)
im = img
default_val = enh[0]
for step in range(2):
    if enh[0] == '#': default_val = {'#':'.','.':'#'}[default_val]
    im = enhance(im,default_val)
    # print_img(im)
part1(Counter(im.values())['#'])

# Part 2
im = img
default_val = enh[0]
for _ in range(50):
    if enh[0] == '#': default_val = {'#':'.','.':'#'}[default_val]
    im = enhance(im,default_val)
part2(Counter(im.values())['#'])