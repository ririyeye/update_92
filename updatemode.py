#!/usr/bin/python3

import ftplib
import os

import paramiko
from scp import SCPClient

from time import sleep
from tcping import Ping
import json
import fileopt
import updatefirmware


def check_cmd_list(ssh, cmds):
    rets = []
    for cmd in cmds:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        ps = stdout.readlines()
        retcode = int(ps[0].strip('\n'))
        rets.append(retcode)

    return rets


def check_rets(rets):
    for ret in rets:
        if ret == 1:
            return True

    return False


def set_updateflg_and_reboot(ssh, remoteip, testmode):
    print(remoteip + "normal mode , need reboot")
    ssh.exec_command("touch /local/sirius-clean-system-flag")
    ssh.exec_command("sync")
    if testmode == 'on':
        sleep(20)
        ssh.exec_command("rm /local/sirius-clean-system-flag")
    else:
        print("reboot " + remoteip)
        updatefirmware.rebootcmd_ssh(ssh)


def change_to_update_mode(remoteip, usr, password, testmode='off', test_program=''):
    print(remoteip + " try update")
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password)

        if test_program == '':
            test_program = []
            test_program.append("ps | grep ar_wdt | grep -v grep | wc -l")

        if not isinstance(test_program, list):
            test_program = [test_program]

        rets = check_cmd_list(ssh, test_program)

        retcode = check_rets(rets)

        if retcode == True:
            set_updateflg_and_reboot(ssh, remoteip, testmode)
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

    ip = '172.16.3.100'

    cmd = 'ps | grep p301d | grep -v grep | wc -l'

    change_to_update_mode(ip, boardusr, boardpass, 'off', test_program=cmd)

    os.system("pause")
