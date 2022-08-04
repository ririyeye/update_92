#!/usr/bin/python3

# from curses import savetty
import fileopt
import updatefirmware
import updatemode

import os
from time import sleep
import json


def update(nodename, force_file='', index=0):
    js = fileopt.get_json_cfg('cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    update_filename = "artosyn-upgrade-sirius-0.0.0.1.img"

    nod = js[nodename]
    remoteip = nod['ip']

    if isinstance(remoteip, list):
        remoteip = remoteip[index]

    upload_filename = update_filename + remoteip

    remote_file = '/tmp/' + update_filename

    boardusr = nod['usr']
    boardpass = nod['pw']

    #check update mode
    updatemode.change_to_update_mode(remoteip, boardusr, boardpass)
    #download update file
    if force_file == '':
        local_file = 'tmp/' + update_filename
        fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass, update_filename, local_file)
    else:
        local_file = force_file

    #check board
    retry = 5
    while retry > 0:
        succ = updatemode.wait_ping(remoteip)
        if float(succ) > 10:
            break
        else:
            print('retry ping' + remoteip)

    remote_file = '/tmp/' + update_filename

    #upload update file
    fileopt.scp_updatefile(remoteip, local_file, remote_file, boardusr, boardpass)
    #update command
    updatefirmware.updatecmd(remoteip, remote_file, boardusr, boardpass)
    #reboot after update
    updatefirmware.rebootcmd(remoteip, boardusr, boardpass)


if __name__ == "__main__":
    update('gnd')

    os.system("pause")
