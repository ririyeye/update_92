#!/usr/bin/python3

import os
import updateonce
import json
import sys
import re


def taketime(elem):
    return elem[0]

def regexproc(dat):
    pat = re.compile('^\[(\d+)\]\[\w+\]\[ALWAYS\] (?:(?!^(?:\[\w+\]){3}).*\n)*', re.MULTILINE)

    timlist = []

    for match in pat.finditer(dat):
        grp = match.group()
        tim = match.group(1)
        timlist.append((tim, grp))

    timlist.sort(key=taketime)

    for logs in timlist:
        print(logs[0], logs[1])


if __name__ == "__main__":

    with open("1.txt", 'r') as f:
        print("read file name = " + f.name)
        dat = f.read()
        regexproc(dat)
    os.system("pause")
