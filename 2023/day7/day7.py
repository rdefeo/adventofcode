#!/usr/bin/env python3

### Advent of Code - 2023 - Day 7

import sys, requests, re, math, itertools, functools, os, collections
from functools import lru_cache
from enum import Enum

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

class Type(Enum):
    FIVE = 1
    FOUR = 2
    FULL = 3
    THREE = 4
    TWO = 5
    ONE = 6
    HIGH = 7
    def __lt__(self, other):
        return self.value < other.value

class Hand:
    def __init__(self,hand):
        cards, bid = hand.split()
        self.orig = cards # actual cards dealt
        self.convert(cards)
        self.bid = int(bid)

    def __repr__(self):
        return self.orig
    
    def convert(self,cards):
        """ Takes the input card hand and converts it to a list of integer values
        for both parts of the problem. For Part 1, the face cards are converted
        as expected. For Part 2, we give the Jacks a value of 1, but then also keep
        track of them to generate the best hand possible. """
        face = {'A':14, 'K':13, 'Q':12, 'J':11, 'T':10}

        # Part 1
        self.cards = [face[c] if c in face else int(c) for c in cards]

        # Part 2 - we not only generate the best hand, but also the hand used for sorting
        self.best_sort = [c if c != 11 else 1 for c in self.cards]
        self.best = [c for c in self.best_sort if c != 1]

        # To generate the best hand, convert the Jacks into the most common card
        jcount = len(self.best_sort) - len(self.best)
        if jcount == 5: # special case
            self.best.append(14)
            jcount -= 1
        self.best += [collections.Counter(self.best).most_common()[0][0]] * jcount

    def type(self, part2=False) -> Type:
        """ Determine the hand type, choosing the original hand or the best hand
        based on which part of the problem we're on """
        cards = self.best if part2 else self.cards
        c = collections.Counter(cards)
        mc = c.most_common()[0][1]
        if mc == 5:
            return Type.FIVE
        elif mc == 4:
            return Type.FOUR
        elif mc == 3:
            if c.most_common()[1][1] == 2:
                return Type.FULL
            return Type.THREE
        elif mc == 2:
            if c.most_common()[1][1] == 2:
                return Type.TWO
            return Type.ONE
        else:
            return Type.HIGH

def compare_hands(a, b, part2=False):
    """ Determine our hand type, based on which part of the problem. For tie breakers,
    use the individual card values or the ones created by the best hand """
    at = a.type(part2)
    bt = b.type(part2)
    if at < bt:
        return -1
    elif at == bt:
        ac = a.best_sort if part2 else a.cards
        bc = b.best_sort if part2 else b.cards
        for i in range(len(ac)):
            if ac[i] == bc[i]:
                continue
            return bc[i] - ac[i]
    return 1

hands = [Hand(h) for h in input_lines]
hsorted = sorted(hands,key=functools.cmp_to_key(compare_hands),reverse=True)
part1(sum((i+1)*h.bid for i, h in enumerate(hsorted)))

hsorted = sorted(hands,key=functools.cmp_to_key(lambda x, y: compare_hands(x,y,True)),reverse=True)
part2(sum((i+1)*h.bid for i, h in enumerate(hsorted)))
