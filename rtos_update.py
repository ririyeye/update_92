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


def update_rtos(nodename, force_file='', index=0):
    js = fileopt.get_json_cfg('cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    upload_filename = debug_filename

    local_file = 'tmp/' + upload_filename

    nod = js[nodename]
    remoteip = nod['ip']
    if isinstance(remoteip, list):
        remoteip = remoteip[index]

    boardusr = nod['usr']
    boardpass = nod['pw']

    if force_file == '':
        remote_file = '/tmp/' + upload_filename
        mem = fileopt.ftpdownload_fo(ftpip, ftpcwd, ftpusr, ftppass, debug_filename)
        fileopt.scp_update_fo(remoteip, mem, remote_file, boardusr, boardpass)
    else:
        remote_file = force_file
        #upload update file
        fileopt.scp_updatefile(remoteip, local_file, remote_file, boardusr, boardpass)

    execcmd(remoteip, boardusr, boardpass)

    updatefirmware.rebootcmd(remoteip, boardusr, boardpass)
