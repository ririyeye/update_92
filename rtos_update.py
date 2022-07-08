

import os
import fileopt

import updatefirmware
import paramiko
from paramiko import SSHClient
from scp import SCPClient

debug_filename = "a7_rtos.nonsec.img"


def execcmd(remoteip, usr, password):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remoteip, 22, usr, password)


    stdin, stdout, stderr = ssh.exec_command(
        "#!/bin/sh \n "
        "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
        "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n"
        "/etc/artosyn-upgrade.sh /tmp/a7_rtos.nonsec.img \n "
        "sleep 1", get_pty=True)

    for line in iter(stdout.readline, ""):
        print(line, end="")

    ssh.close()




def update_rtos(remoteip):
    ftpip = '192.168.200.228'
    ftpcwd = '/export/yangwang'
    ftpusr = 'yangwang'
    ftppass = 'hello,wy'
    # remoteip = '192.168.10.101'
    upload_filename = debug_filename

    boardusr = 'root'
    boardpass = 'artosyn'

    fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass,
                        debug_filename, debug_filename)

    #upload update file
    fileopt.scp_updatefile(remoteip, upload_filename, '/tmp/' +
                           upload_filename, boardusr, boardpass)

    execcmd(remoteip, boardusr, boardpass)
    
    updatefirmware.rebootcmd(remoteip, boardusr, boardpass)
