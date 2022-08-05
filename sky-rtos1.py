#!/usr/bin/python3

import os
import rtos_update
import json
import sys
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            rtos_update.update_rtos('sky', sys.argv[1] , 1)
        else:
            rtos_update.update_rtos('sky', index=1)
    except Exception as err:
        print("error = " , err)
    finally:
        os.system("pause")
