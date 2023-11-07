#!/usr/bin/python3

import asyncio
import os
from pathlib import PurePosixPath
import re

import fileopt
import shutil
import fileopt_aio


def check_all_sdk(name: PurePosixPath, info: list[str]) -> bool:
    reglist = re.compile(r'sdk-artosyn-videowave.*')
    m = reglist.search(name.name)
    if m:
        return True
    return False


if __name__ == "__main__":
    js = fileopt.get_json_cfg('cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    localpath = 'sdk/'

    if os.path.exists(localpath):
        shutil.rmtree(localpath)

    os.mkdir(localpath)

    p = fileopt_aio.ftpdownload_async(ftpip, ftpcwd, ftpusr, ftppass,
                                      check_all_sdk, localpath)
    lo = asyncio.get_event_loop()
    lo.run_until_complete(p)

    os.system("pause")
