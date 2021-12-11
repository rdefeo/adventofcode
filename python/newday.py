#!/usr/bin/env python3

import sys
import os
import requests
import shutil
import argparse
from datetime import date
import re

GREEN = '\033[92m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
LBLUE = '\033[36m'
PURPLE = '\033[35m'
RED = '\033[31m'
CLEAR = '\033[39m'

def status(s):
    print(YELLOW+str(s)+CLEAR)

# generate url for the input day
parser = argparse.ArgumentParser(description='Create a new Advent of Code directory')
parser.add_argument('day',metavar='DAY',type=int,choices=range(1,26),help='Day of the month to create')
parser.add_argument('year',metavar='YEAR',type=int,nargs='?',default=date.today().year,choices=range(2015,date.today().year+1),help='Year of the event. Defaults to current year.')
args = parser.parse_args()

year = args.year
day = args.day

dir = f"day{day}"
full_dir = f"/home/rdefeo/src/advent/{year}/{dir}"

print(f"day = {day}, year = {year}")

if not os.path.exists(full_dir):
    status(f"Generating directory for Day {day}, Event {year}")
    os.makedirs(full_dir)

if os.path.exists(dir+"/.aoc_lock"):
    # we _shouldn't_ get here, because the aoc_newday alias also checks for the .aoc_lock file
    print(PURPLE+f"*** Day {day} was completed and has been locked! ***"+CLEAR)
    print("Aborting")
    quit()

# if not os.path.exists(f"{full_dir}/aoc_utils.py"):
#     os.symlink("/home/rdefeo/src/advent/python/aoc_utils.py",f"{full_dir}/aoc_utils.py")

# always copy the template source and always download input
status(f"Generating template code for Day {day}")
with open("/home/rdefeo/src/advent/python/template.py","r") as src:
    with open(f"{full_dir}/{dir}.py","w") as dest:
        for line in src.readlines():
            if line.startswith("###"):
                line = line.format(year,day)
            dest.write(line)

#shutil.copyfile("template.py",f"{dir}/{dir}.py")
os.chmod(f"{full_dir}/{dir}.py",0o777)

status(f"Downloading input for Day {day}")
url = f"https://adventofcode.com/{year}/day/{day}/input"
cookie = {'session': open('/home/rdefeo/src/advent/.cookie','r').read()}
#status(url)
#status(cookie)
r = requests.post(url,cookies=cookie)
status(f"HTTP Status: {r.status_code}")
if r.status_code == 200:
    #print(str(r.content))
    status("... Writing {} bytes".format(len(r.text)))
    open(f"{full_dir}/input",'wb').write(r.content)
else:
    print(RED+f"... ERROR fetching file at: {url}"+CLEAR)


