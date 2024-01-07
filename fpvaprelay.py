#!/usr/bin/python3

import os
import sys
sys.path.append("..")
import updateonce
import sys

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            updateonce.update("fpvrelay", sys.argv[1])
        else:
            updateonce.update("fpvrelay")
    except Exception as err:
        print("error = ", err)
    finally:
        os.system("pause")
