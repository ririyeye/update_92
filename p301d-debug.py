

import os
import fileopt

import paramiko
from paramiko import SSHClient
from scp import SCPClient

def execcmd(remoteip, usr, password):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remoteip, 22, usr, password)

    stdin, stdout, stderr = ssh.exec_command(
        "#!/bin/sh \n "
        "chmod a+x /tmp/p301d \n "
        "sleep 1", get_pty=True)

    for line in iter(stdout.readline, ""):
        print(line, end="")

    ssh.close()



if __name__ == "__main__":
    ftpip = '192.168.200.228'
    ftpcwd = '/export/yangwang'
    ftpusr = 'yangwang'
    ftppass = 'hello,wy'
    update_filename = "p301d"
    remoteip = '192.168.10.101'
    upload_filename = update_filename

    boardusr = 'root'
    boardpass = 'artosyn'

    fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass,
                        update_filename, update_filename)

    #upload update file
    fileopt.scp_updatefile(remoteip, upload_filename, '/tmp/' +
                           upload_filename, boardusr, boardpass)

    execcmd(remoteip, boardusr, boardpass)

    os.system("pause")
