#!/usr/bin/python3

import os
import rtos_update
import json
import fileopt
import shutil
import sys
if __name__ == "__main__":
    js = fileopt.get_json_cfg('cfg.json')
    nod = js['gnd']

    remoteip = nod['ip']
    if isinstance(remoteip, list):
        remoteip = remoteip[0]    
    
    boardusr = nod['usr']
    boardpass = nod['pw']

    upload_filename = js['filedbg']

    remote_file = '/tmp/' + upload_filename

    if len(sys.argv) > 1:
        local_file = sys.argv[1]
    else:
        local_file = 'tmp/' + upload_filename

    #upload update file
    fileopt.scp_updatefile(remoteip, local_file, remote_file, boardusr, boardpass)

    os.system("pause")
