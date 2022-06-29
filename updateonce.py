

# from curses import savetty
import fileopt
import updatefirmware
import updatemode

import os
from time import sleep

def update(remoteip):
    ftpip='192.168.200.228'
    ftpcwd='/export/yangwang'
    ftpusr='yangwang'
    ftppass='hello,wy'
    update_filename = "artosyn-upgrade-sirius-0.0.0.1.img"

    upload_filename = update_filename+remoteip

    boardusr='root'
    boardpass='artosyn'

#check update mode
    updatemode.change_to_update_mode(remoteip,boardusr,boardpass)
#download update file
    fileopt.ftpdownload(ftpip,ftpcwd,ftpusr,ftppass,update_filename,upload_filename)
#check board
    retry=5
    while retry > 0:
        succ = updatemode.wait_ping(remoteip)
        if float(succ) > 10:
            break
        else:
            print('retry ping' + remoteip)
#upload update file
    fileopt.scp_updatefile(remoteip,upload_filename, boardusr,boardpass)
#update command
    updatefirmware.updatecmd(remoteip,upload_filename,boardusr,boardpass)

if __name__ == "__main__":
    update('192.168.10.101')

    os.system("pause")



    