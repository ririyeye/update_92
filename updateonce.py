#!/usr/bin/python3

# from curses import savetty
import fileopt
import updatefirmware
import updatemode

import os
from time import sleep
import json


def checkboard(remoteip):
    retry = 5
    while retry > 0:
        succ = updatemode.wait_ping(remoteip)
        if float(succ) > 10:
            break
        else:
            print('retry ping' + remoteip)


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
    cmd = ''
    if "test_program" in nod:
        cmd = nod["test_program"]
    updatemode.change_to_update_mode(remoteip, boardusr, boardpass, test_program=cmd)
    #download update file
    remote_file = '/tmp/' + update_filename
    if force_file == '':
        local_file = 'tmp/' + update_filename
        with fileopt.ftpdownload_fo(ftpip, ftpcwd, ftpusr, ftppass, update_filename) as mem:
            checkboard(remoteip)
            fileopt.scp_update_fo(remoteip, mem, remote_file, boardusr, boardpass)
    else:
        local_file = force_file
        checkboard(remoteip)
        fileopt.scp_updatefile(remoteip, local_file, remote_file, boardusr, boardpass)

    #update command
    updatefirmware.updatecmd(remoteip, remote_file, boardusr, boardpass)
    #reboot after update
    updatefirmware.rebootcmd(remoteip, boardusr, boardpass)


if __name__ == "__main__":
    update('testgnd')

    os.system("pause")
