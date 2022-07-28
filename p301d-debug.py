#!/usr/bin/python3

import os
import fileopt

import paramiko
from scp import SCPClient
from time import sleep
import json

# debug_filename = "test_bb_cfg"
debug_filename = "p301d"


def execcmd(remoteip, usr, password):
    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password)

        if debug_filename == "p301d":
            cmds = "/tmp/p301d --board_type 0 --stream_type 1 --pipeline 0 --auto_start | grep debug\n"
        else:
            cmds = "/tmp/" + debug_filename + " \n "

        stdin, stdout, stderr = ssh.exec_command(
            "#!/bin/sh \n "
            "chmod a+x /tmp/" + debug_filename + " \n "
            "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
            + cmds, get_pty=True)

        while not stdout.channel.closed:
            if stdout.channel.recv_ready():
                line = stdout.readline(1024)
                print(line, end="")
            else:
                sleep(0.1)


if __name__ == "__main__":
    js = fileopt.get_json_cfg('cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    gnd = js['sky']
    remoteip = gnd['ip']
    upload_filename = debug_filename

    boardusr = gnd['usr']
    boardpass = gnd['pw']

    fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass,
                        debug_filename, debug_filename)

    #upload update file
    fileopt.scp_updatefile(remoteip, upload_filename, '/tmp/' +
                           upload_filename, boardusr, boardpass)

    #execcmd(remoteip, boardusr, boardpass)

    os.system("pause")
