#!/usr/bin/python3

import os

import paramiko
import updateonce
import json
import sys
import fileopt
import board_tool.httpul
import updatefirmware

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

    board_tool.httpul.httpulfile_sync_wdt(remoteip, 22, boardusr, boardpass)
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, boardusr, boardpass)
        updatefirmware.rebootcmd_ssh(ssh)

    os.system("pause")
