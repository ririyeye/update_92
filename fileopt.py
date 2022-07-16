#!/usr/bin/python3
import ftplib
import os

import paramiko
from paramiko import SSHClient
from scp import SCPClient
import json
import fileopt


class cb_info(object):
    def __init__(self, in_f, in_size):
        self.ftpsize = in_size
        self.f = in_f
        self.download_size = 0

    def callback(self, data):
        self.f.write(data)
        self.download_size = self.download_size + len(data)
        txt = format(self.download_size / self.ftpsize * 100, '.2f') + '%'
        print('\r---'+txt, end="")


def ftpdownload(remoteip, cwd, usr, password, filename, localname):
    print("download " + filename)
    with ftplib.FTP() as ftp:
        ftp.connect(remoteip, 21)
        ftp.login(usr, password)
        ftp.cwd(cwd)
        ftpsize = ftp.size(filename)
        if not os.path.exists('tmp'):
            os.mkdir("tmp")
        with open('tmp/' + localname, 'wb') as f:
            cbi = cb_info(f, ftpsize)
            ftp.retrbinary('RETR ' + filename,
                           cbi.callback, blocksize=128*1024)

    print("download ok!")


def scp_updatefile(remoteip, filename, remote_file, usr, password):
    print("upload updatefile to " + remoteip)
    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remoteip, 22, usr, password)

        # SCPCLient takes a paramiko transport as an argument
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('tmp/' + filename, remote_file)

    print(remoteip + " upload ok")


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

    ftpdownload(ftpip, ftpcwd,
                ftpusr, ftppass, filename, filename)

    boardusr = js['gnd']['usr']
    boardpass = js['gnd']['pw']
    # scp_updatefile('192.168.1.100', filename, '/tmp/' +
    #                filename, boardusr, boardpass)
    # scp_updatefile('192.168.10.101', filename, '/tmp/' +
    #                filename, boardusr, boardpass)
    os.system("pause")
