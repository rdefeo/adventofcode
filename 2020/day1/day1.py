#!/usr/bin/env python3

import os
import sys
import requests

sys.path.append('../../python/')
from aoc_utils import *

start_timer()

# read input data file as array
input = open('input','r').readlines()

e = list(map(int,input))

start_timer('part 1')
for i in range(len(e)):
    for j in range(i+1,len(e)):
        if i+j == 2020:
            print(f"found them {i}, {j}")
            part1(i*j)
            break
    else:
        continue
    break
stop_timer('part 1')

start_timer(2)
part1([a*b for a in e for b in e if a+b==2020])
stop_timer(2)

start_timer(1)
for i in e:
    for j in e:
        for k in e:
            if i == j or i == k or j == k:
                continue
            if i+j+k == 2020:
                print("found them {}, {}, {}".format(i,j,k))
                part2(i*j*k)
                break
        else:
            continue
        break
    else:
        continue
    break
stop_timer(1)


stop_timer()
