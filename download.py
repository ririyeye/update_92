#!/usr/bin/python3

import os

import paramiko
import updateonce
import json
import sys
import fileopt
import board_tool.httpul
import updatefirmware


def execline(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(
        "#!/bin/sh \n "
        "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
        "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n" + cmd + " \n",
        get_pty=True)

    return stdout.readline(1024)

if __name__ == "__main__":
    js = fileopt.get_json_cfg("cfg.json")
    ftpcfg = js["ftp"]

    ftpip = ftpcfg["ip"]
    ftpcwd = ftpcfg["workpath"]
    ftpusr = ftpcfg["usr"]
    ftppass = ftpcfg["pw"]

    nod = js["fpvrelay"]
    remoteip = nod["ip"]

    boardusr = nod["usr"]
    boardpass = nod["pw"]

    local_file = "tmp/" + "lowdelay_relay"
    fileopt.ftpdownload(
        ftpip, ftpcwd, ftpusr, ftppass, "lowdelay_relay", local_file
    )

    board_tool.httpul.httpulfile_sync(remoteip, 22, boardusr, boardpass,local_file,"/tmp/lowdelay_relay")

    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, boardusr, boardpass)
        execline(ssh , "chmod 777 /tmp/lowdelay_relay")

    local_file = "tmp/" + "scp"
    fileopt.ftpdownload(
        ftpip, ftpcwd, ftpusr, ftppass, "scp", local_file
    )

    board_tool.httpul.httpulfile_sync(remoteip, 22, boardusr, boardpass,local_file,"/tmp/scp")

    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, boardusr, boardpass)
        execline(ssh , "chmod 777 /tmp/scp")
        execline(ssh , "mv /tmp/scp /usr/bin/scp")
    
    os.system("pause")
