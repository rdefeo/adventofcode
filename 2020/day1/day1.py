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

# for every element (i) in the expense list (e), find the sum of (i)
# and every element from (i+1) to the end of the list (e). if the sum
# is 2020, multiply them and we're done
start_timer('part 1')
for i in range(len(e)):
    for j in range(i+1,len(e)):
        if e[i]+e[j] == 2020:
            print(f"found them {e[i]}, {e[j]}")
            part1(e[i]*e[j])
            break
    else:
        continue
    break
stop_timer('part 1')

# here's a one-liner way of doing the above! since it loops both
# (a) and (b) across list (e), we get the answer twice: (a*b) and (b*a)
start_timer('part 1 - one liner')
part1([a*b for a in e for b in e if a+b==2020])
stop_timer('part 1 - one liner')

# now do the same as part 1, but do it for 3 values, not 2
start_timer('part 2')
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
stop_timer('part 2')


stop_timer()
