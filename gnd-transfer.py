#!/usr/bin/python3

import os
import debug_transfer
import json

if __name__ == "__main__":
    try:
        debug_transfer.transfer_file('gnd')
    except Exception as err:
        print("error = " , err)
    finally:
        os.system("pause")
