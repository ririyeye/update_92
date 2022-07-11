

import ftplib
import os

import paramiko
from paramiko import SSHClient
from scp import SCPClient

from time import sleep
from tcping import Ping
import json

def change_to_update_mode(remoteip, usr, password, testmode='off'):
    print(remoteip + " try update")
    ssh = SSHClient()
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
            ssh.exec_command(
                "#!/bin/sh \n "
                "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
                "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n"
                "/local/usr/bin/reboot.sh"
            )
            sleep(5)
    else:
        print(remoteip + "enter update mode")

    ssh.close()


def wait_ping(remoteip):
    ping = Ping(remoteip, 22, 1)
    ping.ping(1)
    result = ping.result
    retlist = list(result.raw.split('\n'))
    succ = retlist[2].split(',')[3].split(' ')[1]  # 获取成功率
    return succ.strip('%')


if __name__ == "__main__":
    f = open('cfg.json')
    js = json.load(f)
    board = js['gnd'];
    boardusr = board['usr']
    boardpass = board['pw']
    ip = board['ip']

    change_to_update_mode(ip, boardusr, boardpass, 'off')


    os.system("pause")
