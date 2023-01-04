import os
import json

def get_json_cfg(filename):
    p0 = os.path.realpath(__file__)
    cfgfilename = os.path.join(os.path.dirname(p0), filename)
    with open(cfgfilename) as f:
        return json.load(f)