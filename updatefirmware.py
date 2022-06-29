

import ftplib
import os
from pickle import TRUE

import paramiko
from paramiko import SSHClient
from scp import SCPClient

from time import sleep


def updatecmd(remoteip, file, usr, password):
    print(remoteip + " try update")
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remoteip, 22, usr, password)

    stdin, stdout, stderr = ssh.exec_command(
        "artosyn_upgrade /tmp/" + file, get_pty=True)

    for line in iter(stdout.readline, ""):
        print(line, end="")

    ssh.close()

    print(remoteip + " update ok")


if __name__ == "__main__":
    boardusr = 'root'
    boardpass = 'artosyn'
    updatecmd("192.168.1.100", "artosyn-upgrade-sirius-0.0.0.1.img",
              boardusr, boardpass)
    updatecmd("192.168.10.101", "artosyn-upgrade-sirius-0.0.0.1.img",
              boardusr, boardpass)
    os.system("pause")
