#!/usr/bin/python3

import os

import paramiko
from time import sleep


def execcmd(remoteip, usr, password, cmds):
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password)

        cmd0 = ""
        for line in cmds:
            cmd0 += cmds[line]["cmd"]
        ret = execline(ssh, cmd0)

        i = 0
        for line in cmds:
            tmpstr = ret[i].rstrip("\r\n")
            cmds[line]["val"] = tmpstr
            cmds[line]["valint"] = int(tmpstr, 16)
            i = i+1


def execline(ssh, cmd):
    outline = []
    stdin, stdout, stderr = ssh.exec_command(
        "#!/bin/sh \n "
        "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
        "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n" + cmd + " \n",
        get_pty=True)

    while not stdout.channel.closed:
        if stdout.channel.recv_ready():
            line = stdout.readline(1024)
            if line != "":
                outline += [line]
        else:
            sleep(0.1)
    while True:
        line = stdout.readline(1024)
        if line == "":
            break
        outline += [line]

    return outline


def get_all_reg(boardip, boardusr, boardpass, tab):
    outdict = {}

    cmds = []

    for addr in tab:

        page = addr // 256
        reg = addr % 256
        ra = 0x60680000 + page * 0x100 + reg
        outdict[addr] = {}
        outdict[addr]["addr"] = "0x{:x}".format(ra)
        outdict[addr]["cmd"] = "devmem 0x{:x};".format(ra)

    execcmd(boardip, boardusr, boardpass, outdict)
    return outdict


def get_freq_khz_band(band, rea_val):
    if (band):
        rf_multi = 60 * 1000
    else:
        rf_multi = 30 * 1000

    freq_khz = rf_multi * (rea_val & 0xff)
    reg_d1_d3 = (((rea_val >> 24) & 0xff) | (
        ((rea_val >> 8) & 0xff00)) | (((rea_val << 8) & 0xff0000)))
    remain_val = rf_multi * reg_d1_d3
    remain_val = (remain_val // 16777216)
    freq_khz += remain_val
    return (freq_khz + 1) & 0xfffffffe


def get_freq_khz(val):
    b_2g = get_freq_khz_band(0, val)
    b_5g = get_freq_khz_band(1, val)

    if (b_5g > 5100000 and b_5g < 6000000):
        return b_5g

    return b_2g


fetchtab = [0xd0, 0xd4, 0xd8, 0xdc, 0xe0, 0xe4, 0xe8, 0xec, 0xf0, 0xf4, 0xf8]
fetchtab += [0x154, 0x15c, 0x164, 0x16c, 0x174, 0x17c, 0x184, 0x18c]
fetchtab += [0x04, 0x150]


def print_freq(regdict):
    pridict = [("br", 0xd0), ("fs", 0xd4), ("rx0", 0xd8), ("rx1", 0xdc),
               ("rx2", 0xe0), ("rx3", 0xe4), ("tx0", 0xe8), ("tx1", 0xec), ("tx2", 0xf0), ("tx3", 0xf4), ("csma", 0xf8)]

    for line in pridict:
        freq = get_freq_khz(regdict[line[1]]["valint"])
        print("{0} {1}".format(line[0], freq))


def print_pa(regdict):
    for usr in range(8):
        addr = 0x154 + usr * 8
        val = regdict[addr]["valint"] >> 24 & 0xf
        print("usr {0} 5g = {1} 2g ={2}".format(usr, val >> 2, val & 3))


def get_bw_from_val(val):
    bw = {0: "1.25MHZ", 1: "2.5MHZ", 2: "5MHZ",
          3: "10MHZ", 4: "20MHZ", 5: "40MHZ"}

    try:
        return bw[val]
    except Exception as err:
        return "unknown with reg val = {}".format(val)


def print_bandwidth(regdict):
    val = regdict[0x04]["valint"] >> 24 & 0xff
    val = val >> 4 & 0x07
    print("tx slot0 bw = {}".format(get_bw_from_val(val)))

    val = regdict[0x150]["valint"] >> 24 & 0xff
    val = val & 0x07
    print("rx slot0 bw = {}".format(get_bw_from_val(val)))


if __name__ == "__main__":
    boardusr = 'root'
    boardpass = 'artosyn'
    boardip = '192.168.10.100'

    regdict = get_all_reg(boardip, boardusr, boardpass, fetchtab)

    print_freq(regdict)

    print_pa(regdict)

    print_bandwidth(regdict)

    os.system("pause")
