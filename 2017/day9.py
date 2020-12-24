#!/usr/bin/env python3

import re

# group { }
# garbage < >

input = open('day9.txt','r').read().strip()

def score_string(s):
    ingroup = False
    ingarbage = False

    # score of the current group (goes up and down based on entering /
    # leaving groups)
    group_score_value = 0
    group_score = 0
    garbage_count = 0

    i = 0
    while i < len(s):
        if s[i] == '{' and not ingarbage:
            ingroup = True
            group_score_value += 1
        elif s[i] == '}' and not ingarbage:
            ingroup = False
            ingarbage = False
            group_score += group_score_value
            group_score_value -= 1
        elif s[i] == '!':
            i += 1
        elif s[i] == '<':
            if ingarbage:
                garbage_count += 1
            else:
                ingarbage = True
        elif s[i] == '>':
            ingarbage = False
        else:
            # random character
            if ingarbage:
                garbage_count += 1
            pass
        i += 1
    print("garbage count: ",garbage_count)
    return group_score

# print(score_string('{}'))
# print(score_string('{{{}}}'))
# print(score_string('{{},{}}'))
# print(score_string('{{{},{},{{}}}}'))
# print(score_string('{<a>,<a>,<a>,<a>}'))
# print(score_string('{{<ab>},{<ab>},{<ab>},{<ab>}}'))
# print(score_string('{{<!!>},{<!!>},{<!!>},{<!!>}}'))
# print(score_string('{{<a!>},{<a!>},{<a!>},{<ab>}}'))

print(score_string('<>'))
print(score_string('<random characters>'))
print(score_string('<<<<>'))
print(score_string('<{!>}>'))
print(score_string('<!!>'))
print(score_string('<!!!>>'))
print(score_string('<{o"i!a,<{i<a>'))

print(score_string(input))
