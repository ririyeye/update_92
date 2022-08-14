#!/usr/bin/python3

from operator import mod
import os
import fileopt
import sys

import paramiko
from scp import SCPClient
from time import sleep
import json



if __name__ == "__main__":
    js = fileopt.get_json_cfg('cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    boardtyp = 'sky'

    gnd = js[boardtyp]
    remoteip = gnd['ip']
    debugnode = js['p301d']

    upload_filename = debugnode["file"]
    remote_filename = '/tmp/' + upload_filename

    boardusr = gnd['usr']
    boardpass = gnd['pw']

    if len(sys.argv) > 1:
        local_file = sys.argv[1]
    else:
        local_file = 'tmp/' + upload_filename
        fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass, upload_filename, local_file)

    #upload update file
    fileopt.scp_updatefile(remoteip, local_file, remote_filename, boardusr, boardpass)

    fileopt.execcmds(remoteip, boardusr, boardpass, debugnode['com'])

    os.system("pause")
