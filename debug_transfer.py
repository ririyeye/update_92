#!/usr/bin/python3

import os
import fileopt

import updatefirmware
import paramiko
from scp import SCPClient
import json
from time import sleep





def transfer_file(nodename):
    js = fileopt.get_json_cfg('cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    upload_filename = js['transferdbg']['file']

    nod = js[nodename]

    remoteip = nod['ip']
    if isinstance(remoteip, list):
        remoteip = remoteip[0]    
    
    boardusr = nod['usr']
    boardpass = nod['pw']

    local_file = 'tmp/' + upload_filename
    remote_file = '/tmp/' + upload_filename

    fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass, upload_filename, local_file)

    #upload update file
    fileopt.scp_updatefile(remoteip, local_file, remote_file, boardusr, boardpass)

    cmds = js['transferdbg'][nodename]

    fileopt.execcmd(remoteip, boardusr, boardpass, cmds)

    # updatefirmware.rebootcmd(remoteip, boardusr, boardpass)
