#!/usr/bin/python3

import os
import rtos_update
import json
import fileopt
import shutil
if __name__ == "__main__":
    js = fileopt.get_json_cfg('cfg.json')
    nod = js['sky']

    remoteip = nod['ip']
    boardusr = nod['usr']
    boardpass = nod['pw']

    upload_filename = js['filedbg']

    shutil.copyfile(upload_filename, 'tmp/' + upload_filename)

    #upload update file
    fileopt.scp_updatefile(remoteip, upload_filename, '/tmp/' + upload_filename, boardusr, boardpass)
    os.system("pause")
