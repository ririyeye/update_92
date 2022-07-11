

import ftplib
import os
from pickle import TRUE

import paramiko
from paramiko import SSHClient
from scp import SCPClient

from time import sleep
import json

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


def rebootcmd(remoteip, usr, password):
    print(remoteip + " try reboot")
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remoteip, 22, usr, password ,timeout=10)

    stdin, stdout, stderr = ssh.exec_command(
        "#!/bin/sh \n "
        "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
        "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n"
        "cp /local/usr/bin/ar_wdt_service /tmp \n "
        "/tmp/ar_wdt_service -t 1 & \n "
        # "sleep 1  \n "
        "devmem 0x606330b4 32 0x04912028 \n"
        "echo 15 > /sys/class/gpio/export \n"
        "echo \"out\" > /sys/class/gpio/gpio15/direction \n "
        "echo 0 > /sys/class/gpio/gpio15/value \n"
        "ps \n "
        "killall ar_wdt_service \n "
        , get_pty=True)

    for line in iter(stdout.readline, ""):
        print(line, end="")

    ssh.close()

    print(remoteip + " reboot ok")


if __name__ == "__main__":
    f = open('cfg.json')
    js = json.load(f)
    board = js['gnd'];
    boardusr = board['usr']
    boardpass = board['pw']
    ip = board['ip']
    # updatecmd("192.168.1.100", "artosyn-upgrade-sirius-0.0.0.1.img",
    #           boardusr, boardpass)
    # updatecmd("192.168.10.101", "artosyn-upgrade-sirius-0.0.0.1.img",
    #           boardusr, boardpass)
    rebootcmd(ip, boardusr, boardpass)

    os.system("pause")
