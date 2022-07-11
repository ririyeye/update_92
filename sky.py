

import os
import updateonce
import json

if __name__ == "__main__":
    f = open('cfg.json')
    js = json.load(f)
    updateonce.update(js['sky']['ip'])

    os.system("pause")
