#!/usr/bin/python3

import os
import updateonce
import json
import sys

import paramiko
from scp import SCPClient
from time import sleep
import io

def execcmd(remoteip, usr, password, cmds):
    output = []
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password)

        for line in cmds:
            ret = execline(ssh, line)
            output.append((line , ret))

    return output


def execline(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(
        "#!/bin/sh \n "
        "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
        "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n" + cmd + " \n",
        get_pty=True)

    return stdout.readline(1024)



if __name__ == "__main__":
    boardusr = 'root'
    boardpass = 'artosyn'
    boardip = '192.168.10.100'

    cmd = ""

    for page in range(0,3):
        for addr in range(0,64):
            ra = 0x60680000 + page * 0x100 + addr * 4
            cmd += "devmem 0x{:x};".format(ra)

    output = execcmd(boardip,boardusr,boardpass,[cmd])

    for out in output:
        print(out[0].lstrip('devmem '),":",out[1].rstrip('\n'))
