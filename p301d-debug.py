#!/usr/bin/python3

from operator import mod
import os
import fileopt

import paramiko
from scp import SCPClient
from time import sleep
import json


def execcmd(remoteip, usr, password, cmd):
    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password)
        fileopt.execline(ssh,cmd)



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

    debug_filename = debugnode["file"]
    upload_filename = debug_filename

    boardusr = gnd['usr']
    boardpass = gnd['pw']

    fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass,
                        debug_filename, debug_filename)

    #upload update file
    fileopt.scp_updatefile(remoteip, upload_filename, '/tmp/' +
                           upload_filename, boardusr, boardpass)

    for line in debugnode['com']:
        execcmd(remoteip, boardusr, boardpass, line)

    os.system("pause")
