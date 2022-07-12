#!/usr/bin/python3

import os
import rtos_update
import json

if __name__ == "__main__":
    rtos_update.update_rtos('gnd')

    os.system("pause")
