#!/usr/bin/python3

import os
import rtos_update
import json
import sys
if __name__ == "__main__":
    if len(sys.argv) > 1:
        rtos_update.update_rtos('sky', sys.argv[1])
    else:
        rtos_update.update_rtos('sky')

    os.system("pause")
