#!/usr/bin/python3

import os
import updateonce
import json
import sys

import paramiko
from scp import SCPClient
from time import sleep
import io
import time


def execline2(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(
        "#!/bin/sh \n "
        "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
        "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n" + cmd + " \n",
        get_pty=True)

    out = ""

    while not stdout.channel.closed:
        if stdout.channel.recv_ready():
            line = stdout.readline(10240)
            out += line
        else:
            sleep(0.1)

    while True:
        ret2 = stdout.readline()
        if ret2 == "":
            break
        out += ret2

    return out


def reset_bit(ssh,addr,bit):
    ra = 0x60680000 + addr
    # get val
    cmd0 = "devmem 0x{:x} 32".format(ra)
    out = execline2(ssh,cmd0)
    dat = int(out,16)
    # set bit
    dat1 = dat | (1 << bit)
    cmd1 = "devmem 0x{:x} 32 0x{:x}".format(ra,dat1)
    out = execline2(ssh,cmd1)
    # reset bit
    cmd2 = "devmem 0x{:x} 32 0x{:x}".format(ra,dat)
    out = execline2(ssh,cmd2)

def get_bit(ssh,addr ,bit):
    ra = 0x60680000 + addr
    # get val
    cmd = "devmem 0x{:x} 32".format(ra)
    out = execline2(ssh,cmd)
    dat = int(out,16)
    return dat & (1 << bit)

def dump(ssh,filename):
    cmd = ""

    for page in range(0,3):
        for addr in range(0,64):
            ra = 0x60680000 + page * 0x100 + addr * 4
            cmd += "echo 0x{:x} $(devmem 0x{:x});".format(ra,ra)

    ret = execline2(ssh, cmd)
    with open(filename , 'w') as f:
        f.truncate()
        f.write(ret)

def debugmode(ssh):
    ret = execline2(ssh, "/local/usr/bin/rtcmd debug_mode ; sleep 1")
    return ret



if __name__ == "__main__":
    boardusr = 'root'
    boardpass = 'artosyn'
    boardip = '192.168.10.100'

    cmd = ""

    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(boardip, 22, boardusr, boardpass)
        dump(ssh,'before.txt')
        resetcnt = 0
        while 1 :
            reset_bit(ssh,0,2)
            resetcnt += 1
            brunlock = 0
            for i in range(0,10):
                time.sleep(0.02)
                ret = get_bit(ssh,0x5dc,1)
                if ret == 0: 
                    brunlock += 1

            if brunlock == 10 :
                ppp = debugmode(ssh)
                print(ppp)
                dump(ssh,'after.txt')
                break

        print("reset = " , resetcnt)
    
