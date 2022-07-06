

import os
import fileopt

import paramiko
from paramiko import SSHClient
from scp import SCPClient

# debug_filename = "test_bb_cfg"
debug_filename = "p301d"


def execcmd(remoteip, usr, password):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remoteip, 22, usr, password)

    if debug_filename == "p301d":
        cmds = "/tmp/p301d --board_type 0 --stream_type 1 --pipeline 0 --auto_start | grep debug\n"
    else:
        cmds = "/tmp/" + debug_filename + " \n "

    stdin, stdout, stderr = ssh.exec_command(
        "#!/bin/sh \n "
        "chmod a+x /tmp/" + debug_filename + " \n "
        "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
        + cmds +
        "sleep 1", get_pty=True)

    for line in iter(stdout.readline, ""):
        print(line, end="")

    ssh.close()


if __name__ == "__main__":
    ftpip = '192.168.200.228'
    ftpcwd = '/export/yangwang'
    ftpusr = 'yangwang'
    ftppass = 'hello,wy'
    remoteip = '192.168.10.101'
    upload_filename = debug_filename

    boardusr = 'root'
    boardpass = 'artosyn'

    fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass,
                        debug_filename, debug_filename)

    #upload update file
    fileopt.scp_updatefile(remoteip, upload_filename, '/tmp/' +
                           upload_filename, boardusr, boardpass)

    execcmd(remoteip, boardusr, boardpass)

    os.system("pause")
