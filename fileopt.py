#!/usr/bin/python3
import ftplib
import os

import paramiko
from scp import SCPClient
import json
import fileopt
from time import sleep


class cb_info(object):

    def __init__(self, in_f, in_size):
        self.ftpsize = in_size
        self.f = in_f
        self.download_size = 0

    def callback(self, data):
        self.f.write(data)
        self.download_size = self.download_size + len(data)
        txt = format(self.download_size / self.ftpsize * 100, '.2f') + '%'
        print('\r---' + txt, end="")


def ftpdownload(remoteip, cwd, usr, password, server_filename, localname):
    print("download " + server_filename)
    with ftplib.FTP() as ftp:
        ftp.connect(remoteip, 21)
        ftp.login(usr, password)
        ftp.cwd(cwd)
        ftpsize = ftp.size(server_filename)

        path = os.path.dirname(localname)
        if not os.path.exists(path):
            os.mkdir(path)

        with open(localname, 'wb') as f:
            cbi = cb_info(f, ftpsize)
            ftp.retrbinary('RETR ' + server_filename, cbi.callback, blocksize=128 * 1024)

    print("download ok!")


def scp_updatefile(remoteip, local_file, remote_file, usr, password):
    print("upload updatefile to " + remoteip)
    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password)

        def cb(local_file, size, sent):
            percent = format(sent / size * 100, '.2f') + '%'
            print("\rcopy ", local_file, percent, end="")

        # SCPCLient takes a paramiko transport as an argument
        with SCPClient(ssh.get_transport(), progress=cb) as scp:
            scp.put(local_file, remote_file)
        print("\n")

    print(remoteip + " upload ok")

def execcmd(remoteip, usr, password, cmds):
    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password)

        for line in cmds:
            fileopt.execline(ssh, line)

def execline(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(
        "#!/bin/sh \n "
        "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
        "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n" + cmd + " \n",
        get_pty=True)

    print("exec " + cmd)
    while not stdout.channel.closed:
        if stdout.channel.recv_ready():
            line = stdout.readline(1024)
            print(line, end="")
        else:
            sleep(0.1)

    print(stdout.readline())


def get_json_cfg(filename):
    p0 = os.path.realpath(__file__)
    cfgfilename = os.path.join(os.path.dirname(p0), filename)
    with open(cfgfilename) as f:
        return json.load(f)


if __name__ == "__main__":
    filename = "a7_rtos.nonsec.img"
    js = get_json_cfg('cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    ftpdownload(ftpip, ftpcwd, ftpusr, ftppass, filename, filename)

    board = js['gnd']

    boardusr = board['usr']
    boardpass = board['pw']
    boardip = board['ip']

    scp_updatefile(boardip, 'tmp/' + filename, '/tmp/' + filename, boardusr, boardpass)
    os.system("pause")
