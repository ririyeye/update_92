#!/usr/bin/python3

import ftplib
import os

import paramiko
from paramiko import SSHClient
from scp import SCPClient

from time import sleep
from tcping import Ping
import json
import fileopt
import updatefirmware
def change_to_update_mode(remoteip, usr, password, testmode='off'):
    print(remoteip + " try update")
    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password)

        stdin, stdout, stderr = ssh.exec_command(
            "ps | grep 301d | grep -v grep | wc -l")
        ps = stdout.readlines()
        retcode = int(ps[0].strip('\n'))

        if retcode == 1:
            print(remoteip + "normal mode , need reboot")
            ssh.exec_command("touch /local/sirius-clean-system-flag")
            ssh.exec_command("sync")
            if testmode == 'on':
                sleep(20)
                ssh.exec_command("rm /local/sirius-clean-system-flag")
            else:
                print("reboot " + remoteip)
                updatefirmware.rebootcmd_ssh(ssh)
        else:
            print(remoteip + "enter update mode")


def wait_ping(remoteip):
    ping = Ping(remoteip, 22, 1)
    ping.ping(1)
    result = ping.result
    retlist = list(result.raw.split('\n'))
    succ = retlist[2].split(',')[3].split(' ')[1]  # 获取成功率
    return succ.strip('%')


if __name__ == "__main__":
    js = fileopt.get_json_cfg('cfg.json')
    board = js['gnd']
    boardusr = board['usr']
    boardpass = board['pw']
    ip = board['ip']

    change_to_update_mode(ip, boardusr, boardpass, 'off')

    os.system("pause")
