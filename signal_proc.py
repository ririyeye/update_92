#!/usr/bin/python3

import os
import updateonce
import json
import sys
import re

def regexproc(str0):
    pat = re.compile('\\[(\\d+\\.\\d+)\\]')
    last = 0
    for match in pat.finditer(str0):
        g1 = match.group(0)
        g2 = match.group(1)

        if(float(g2) - last > 0.01) :
            print(g2)
        last = float(g2)

if __name__ == "__main__":
    with open("after.txt", 'r') as f0:
        str0 = f0.read()
        regexproc(str0)