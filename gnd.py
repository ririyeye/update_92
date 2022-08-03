#!/usr/bin/python3

import os
import updateonce
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        updateonce.update('gnd', sys.argv[1])
    else:
        updateonce.update('gnd')

    os.system("pause")
