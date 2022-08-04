#!/usr/bin/python3

import os
import updateonce
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        updateonce.update('sky', sys.argv[1] , 1)
    else:
        updateonce.update('sky', index=1)

    os.system("pause")
