#!/usr/bin/python3

from distutils import filelist
import os
import updateonce
import json
import sys
import fileopt
import shutil
import asyncio
from aio import ftpdl

if __name__ == "__main__":
    js = fileopt.get_json_cfg('cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    file_list = js['pull_img']

    localpath = 'sdk/'

    if os.path.exists(localpath):
        shutil.rmtree(localpath)
        
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    path = os.path.dirname(localpath + file_list[0])
    if not os.path.exists(path):
        os.mkdir(path)
    
    tasks = [loop.create_task(ftpdl.ftp_dl_file(ftpip, ftpcwd, ftpusr, ftppass, file,localpath + file)) for file in file_list]
    
    loop.run_until_complete(asyncio.gather(*tasks))

    os.system("pause")
