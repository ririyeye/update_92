
import ftplib
import os

import paramiko
from paramiko import SSHClient
from scp import SCPClient


# filename = "artosyn-upgrade-sirius-0.0.0.1.img"


def ftpdownload(remoteip, cwd, usr, password, filename, localname):
    print("download " + filename)
    ftp = ftplib.FTP()
    ftp.connect(remoteip, 21)
    ftp.login(usr, password)
    ftp.cwd(cwd)

    with open(localname, 'wb') as f:
        ftp.retrbinary('RETR ' + filename, f.write)

    print("download ok!")


def scp_updatefile(remoteip, filename, usr, password):
    print("upload updatefile to " + remoteip)
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remoteip, 22, usr, password)

    # SCPCLient takes a paramiko transport as an argument
    scp = SCPClient(ssh.get_transport())
    scp.put(filename, '/tmp/' + filename)
    scp.close()
    print(remoteip + " upload ok")


if __name__ == "__main__":
    filename = "artosyn-upgrade-sirius-0.0.0.1.img"
    ftpdownload('192.168.200.228', '/export/yangwang',
                'yangwang', 'hello,wy', filename, filename)

    boardusr = 'root'
    boardpass = 'artosyn'
    # scp_updatefile('192.168.1.100',filename ,boardusr,boardpass)
    # scp_updatefile('192.168.10.101',filename , boardusr,boardpass)
    os.system("pause")
