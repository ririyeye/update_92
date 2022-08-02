#!/usr/bin/python3

from distutils import filelist
import os
import updateonce
import json
import sys
import fileopt
import shutil


if __name__ == "__main__":
    js = fileopt.get_json_cfg('cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    file_list = js['pull_sdk']

    localpath = 'sdk/'

    if os.path.exists(localpath):
        shutil.rmtree(localpath)

    for file in file_list:
        fileopt.ftpdownload(ftpip, ftpcwd, ftpusr, ftppass, file, localpath + file)

    os.system("pause")
