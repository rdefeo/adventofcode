#!/usr/bin/env python3

### Advent of Code - 2023 - Day 24

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
import random

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
#input_nums = list(map(int,input_lines))

class Vector3:
    def __init__(self,v):
        self.x = v[0]
        self.y = v[1]
        self.z = v[2]
    def cross(self,v):
        x = self.y*v.z-self.z*v.y
        y = self.z*v.x-self.x*v.z
        z = self.x*v.y-self.y*v.x
        return Vector3([x,y,z])
    def dot(self,v):
        return self.x*v.x + self.y*v.y + self.z*v.z
    def mag(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    def __repr__(self):
        return f"({self.x},{self.y},{self.z})"
class Hail:
    def __init__(self,p,v):
        self.p = Vector3(p)
        self.v = Vector3(v)
        self.rise = v[1]
        self.run = v[0]
        self.m = self.rise / self.run
        self.b = p[1] - self.m * p[0]
        
    def pos_at_time(self,t):
        return Vector3([self.p.x+(t*self.v.x),self.p.y+(t*self.v.y),self.p.z+(t*self.v.z)])
    
    def __repr__(self):
        # return f"{{p={self.p}, v={self.v}, y = {self.m}x + {self.b}}}"
        return f"{{p={self.p}, v={self.v}}}"

hail = []
for line in input_lines:
    nums = list(map(int,re.findall(r"-?\d+",line)))
    hail.append(Hail(nums[:3],nums[3:]))
# print(hail)

LOWER = 7
UPPER = 27
LOWER = 200000000000000
UPPER = 400000000000000

in_box = 0
for i in range(len(hail)):
    m1, b1 = hail[i].m, hail[i].b
    for j in range(i+1,len(hail)):
        # check for intersection
        m2, b2 = hail[j].m, hail[j].b
        if m2-m1 == 0:
            # print(f"{hail[i]} and {hail[j]} have same slopes - don't intersect!")
            continue
        x = (b1 - b2) / (m2 - m1)
        y = m1 * x + b1
        # print(f"Hail {hail[i]} and {hail[j]} intersect at {x:.3f},{y:.3f}")
        if LOWER <= x <= UPPER and LOWER <= y <= UPPER:
            # print("  in the box!")
            # our intersection is inside the box, but did it happen in the future or past?
            # must check _both_ hail stones
            if (
                (((x > hail[i].p.x and hail[i].run > 0) or
                (x < hail[i].p.x and hail[i].run < 0)) and
                ((y > hail[i].p.y and hail[i].rise > 0) or
                (y < hail[i].p.y and hail[i].rise < 0))) and
                (((x > hail[j].p.x and hail[j].run > 0) or
                (x < hail[j].p.x and hail[j].run < 0)) and
                ((y > hail[j].p.y and hail[j].rise > 0) or
                (y < hail[j].p.y and hail[j].rise < 0)))
            ):
                # print("    in the future! success!")
                in_box += 1
            else:
                # print("    must be the past")
                pass
        else:
            # print("  not in the box :(")
            pass
part1(in_box)

def find_rock():
    h1 = hail[0]
    h2 = hail[1]
    
    for vx in range(-300,300):
        for vy in range(-300,300):
            for vz in range(-300,300):
                if vx * vy * vz == 0: continue
                # With this given velocity, adjust the hail velocity to the rocks frame
                # The aim is to have the hail fly towards a stationary rock - assuming
                # we have found the correct velocity for the rock.
                # 
                # Each hail will interset at different times: t and u. Let's try to find
                # a 2D solution first (in x-y plane) and see if that works for all hail
                # in 3D. 
                #
                # These two hailstones should intersect if the velocity is correct
                h1_vx = h1.v.x - vx
                h1_vy = h1.v.y - vy

                h2_vx = h2.v.x - vx
                h2_vy = h2.v.y - vy

                if (h1_vx*h2_vy - h1_vy*h2_vx) == 0:
                    continue
                
                t = (h2_vy * (h2.p.x - h1.p.x) - h2_vx * (h2.p.y - h1.p.y)) / (h1_vx*h2_vy - h1_vy*h2_vx)
                
                x = h1.p.x + h1.v.x * t - vx * t
                y = h1.p.y + h1.v.y * t - vy * t
                z = h1.p.z + h1.v.z * t - vz * t

                # does every hail stone intersect at this location? that is, are
                # points x,y on this hailstone's line? Compute u, which is the time
                # required to reach this point at the hailstone's new velocity. This
                # can be computed by checking any of the dimensions
                hitall = True
                for h in hail:
                    u = 0
                    if h.v.x != vx: # prevent div/0
                        u = (x - h.p.x) / (h.v.x - vx)
                    elif h.v.y != vy:
                        u = (y - h.p.y) / (h.v.y - vy)
                    else:
                        u = (z - h.p.z) / (h.v.z - vz)
                    
                    if x+u*vx != h.p.x+u*h.v.x or y+u*vy != h.p.y+u*h.v.y or z+u*vz != h.p.z+u*h.v.z:
                        hitall = False
                        break

                if hitall:
                    print(x,y,z,vx,vy,vz)
                    part2(int(x+y+z))
                    exit()
    return None

find_rock()