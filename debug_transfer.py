#!/usr/bin/python3

import os
import fileopt

import updatefirmware
import paramiko
from scp import SCPClient
import json
from time import sleep


def execline(ssh , cmd):
    stdin, stdout, stderr = ssh.exec_command(
        "#!/bin/sh \n "
        "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
        "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n"
        + cmd + " \n", get_pty=True)

    print("exec " + cmd)
    readflg = 0
    while not stdout.channel.closed:
        if stdout.channel.recv_ready():
            line = stdout.readline(1024)
            print(line, end="")
            readflg = 1
        else:
            sleep(0.1)

    print(stdout.readline())

def execcmd(remoteip, usr, password ,cmdfile , cmds):
    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password)

        for line in cmds:
            execline(ssh , line)



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
    boardusr = nod['usr']
    boardpass = nod['pw']

    fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass,
                        upload_filename, upload_filename)

    #upload update file
    fileopt.scp_updatefile(remoteip, upload_filename, '/tmp/' +
                           upload_filename, boardusr, boardpass)

    cmds = js['transferdbg'][nodename]

    execcmd(remoteip, boardusr, boardpass, upload_filename, cmds)

    # updatefirmware.rebootcmd(remoteip, boardusr, boardpass)
