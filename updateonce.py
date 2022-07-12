

# from curses import savetty
import fileopt
import updatefirmware
import updatemode

import os
from time import sleep
import json


def update(nodename):
    f = open('cfg.json')
    js = json.load(f)
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    update_filename = "artosyn-upgrade-sirius-0.0.0.1.img"

    nod = js[nodename]
    remoteip = nod['ip']

    upload_filename = update_filename+remoteip

    boardusr = nod['usr']
    boardpass = nod['pw']

#check update mode
    updatemode.change_to_update_mode(remoteip, boardusr, boardpass)
#download update file
    fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass,
                        update_filename, upload_filename)
#check board
    retry = 5
    while retry > 0:
        succ = updatemode.wait_ping(remoteip)
        if float(succ) > 10:
            break
        else:
            print('retry ping' + remoteip)
#upload update file
    fileopt.scp_updatefile(remoteip, upload_filename,
                           '/tmp/' + upload_filename, boardusr, boardpass)
#update command
    updatefirmware.updatecmd(remoteip, upload_filename, boardusr, boardpass)
#reboot after update
    updatefirmware.rebootcmd(remoteip, boardusr, boardpass)


if __name__ == "__main__":
    update('gnd')

    os.system("pause")
