#!/usr/bin/python3

import os
import updateonce
import json
import sys
import re


def taketime(elem):
    return elem[0]


def regexproc(gnd, sky):
    pat = re.compile('^\[(\d+)\]\[\w+\]\[[A-Z]+\] \[(\d+)\] (?:(?!^(?:\[\w+\]){3} \[\d+\]).*\n)*', re.MULTILINE)
    timlist = []

    for match in pat.finditer(gnd):
        grp = match.group()
        tim = match.group(1)
        timlist.append((tim, 'gnd', grp))

    for match in pat.finditer(sky):
        grp = match.group()
        tim = match.group(2)
        timlist.append((tim, 'sky', grp))

    timlist.sort(key=taketime)
    lastdev = 'null'
    with open("out.txt", 'w') as f:
        f.truncate()
        for logs in timlist:
            if lastdev != str(logs[1]):
                lastdev = str(logs[1])
                f.write('\n\n')
            else:
                f.write('\n')

            f.write(logs[0])
            f.write(' ')
            f.write(logs[1])
            f.write(' ')
            write2 = str(logs[2]).rstrip('\n')
            f.write(write2)

if __name__ == "__main__":
    with open("gnd.txt", 'r') as f0, open("sky.txt", 'r') as f1:
        gnd = f0.read()
        sky = f1.read()
        regexproc(gnd, sky)
    # os.system("pause")
