#!/usr/bin/python3

import ftplib
import os
from pickle import TRUE

import paramiko
from scp import SCPClient

from time import sleep
import json
import fileopt


def updatecmd(remoteip, file, usr, password):
    print(remoteip + " try update")
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password)

        stdin, stdout, stderr = ssh.exec_command(
            "#!/bin/sh \n "
            "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
            "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n"
            "artosyn_upgrade " + file,
            get_pty=True,
        )

        while not stdout.channel.closed:
            if stdout.channel.recv_ready():
                line = stdout.readline(1024)
                print(line, end="")
            else:
                sleep(0.1)

        while True:
            line = stdout.readline(1024)
            if line == "":
                break
            print(line, end="")

    print(remoteip + " update ok")


def rebootcmd_ssh(ssh):
    stdin, stdout, stderr = ssh.exec_command(
        "#!/bin/sh \n "
        "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
        "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n"
        "/tmp/ar_wdt_service2 -t 1 & \n "
        # "sleep 1  \n "
        "devmem 0x606330b4 32 0x04912028 \n"
        "echo 15 > /sys/class/gpio/export \n"
        'echo "out" > /sys/class/gpio/gpio15/direction \n '
        "echo 0 > /sys/class/gpio/gpio15/value \n"
        "ps \n "
        "killall ar_wdt_service2 \n ",
        get_pty=True,
    )
    sleep(5)


def rebootcmd(remoteip, usr, password):
    print(remoteip + " try reboot")
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password, timeout=10)

        rebootcmd_ssh(ssh)

    print(remoteip + " reboot ok")


if __name__ == "__main__":
    js = fileopt.get_json_cfg("cfg.json")
    board = js["gnd"]
    boardusr = board["usr"]
    boardpass = board["pw"]
    ip = board["ip"]
    # updatecmd("192.168.1.100", "artosyn-upgrade-sirius-0.0.0.1.img",
    #           boardusr, boardpass)
    # updatecmd("192.168.10.101", "artosyn-upgrade-sirius-0.0.0.1.img",
    #           boardusr, boardpass)
    rebootcmd(ip, boardusr, boardpass)

    os.system("pause")
