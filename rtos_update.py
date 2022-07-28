#!/usr/bin/python3

import os
import fileopt

import updatefirmware
import paramiko
from scp import SCPClient
import json
from time import sleep

debug_filename = "a7_rtos.nonsec.img"


def execcmd(remoteip, usr, password):
    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password)

        stdin, stdout, stderr = ssh.exec_command(
            "#!/bin/sh \n "
            "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
            "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n"
            "/etc/artosyn-upgrade.sh /tmp/a7_rtos.nonsec.img \n ",
            get_pty=True)

        while not stdout.channel.closed:
            if stdout.channel.recv_ready():
                line = stdout.readline(1024)
                print(line, end="")
            else:
                sleep(0.1)


def update_rtos(nodename):
    js = fileopt.get_json_cfg('cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    upload_filename = debug_filename

    nod = js[nodename]

    remoteip = nod['ip']
    boardusr = nod['usr']
    boardpass = nod['pw']

    fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass, debug_filename, debug_filename)

    #upload update file
    fileopt.scp_updatefile(remoteip, upload_filename, '/tmp/' + upload_filename, boardusr, boardpass)

    execcmd(remoteip, boardusr, boardpass)

    updatefirmware.rebootcmd(remoteip, boardusr, boardpass)
