
import ftplib
import os

import paramiko
from paramiko import SSHClient
from scp import SCPClient
import json

# filename = "artosyn-upgrade-sirius-0.0.0.1.img"
download_size = 0


def ftpdownload(remoteip, cwd, usr, password, filename, localname):
    print("download " + filename)
    ftp = ftplib.FTP()
    ftp.connect(remoteip, 21)
    ftp.login(usr, password)
    ftp.cwd(cwd)
    ftpsize = ftp.size(filename)
    with open(localname, 'wb') as f:
        def callback(data):
            global download_size
            f.write(data)
            download_size = download_size + len(data)
            txt = format(download_size / ftpsize * 100, '.2f') + '%'
            print('\r---'+txt,end="")
        ftp.retrbinary('RETR ' + filename, callback)

    print("download ok!")


def scp_updatefile(remoteip, filename, remote_file, usr, password):
    print("upload updatefile to " + remoteip)
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remoteip, 22, usr, password)

    # SCPCLient takes a paramiko transport as an argument
    scp = SCPClient(ssh.get_transport())
    scp.put(filename, remote_file)
    scp.close()
    ssh.close()
    print(remoteip + " upload ok")


if __name__ == "__main__":
    filename = "artosyn-upgrade-sirius-0.0.0.1.img"
    f = open('cfg.json')
    js = json.load(f)
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
