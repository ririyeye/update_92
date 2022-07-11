

import os
import rtos_update
import json
if __name__ == "__main__":
    f = open('cfg.json')
    js = json.load(f)

    rtos_update.update_rtos(js['sky']['ip'])

    os.system("pause")
