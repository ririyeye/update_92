#!/usr/bin/python3

import os

import updatefirmware
import json
import asyncio
from aio import execline
from aio import ftpdl
from aio import scpul
from aio import coms

import tempfile

debug_filename = "a7_rtos.nonsec.img"

updatecmd = '/etc/artosyn-upgrade.sh /tmp/a7_rtos.nonsec.img \n'


async def _update_rtos(nodename, force_file='', index=0):
    js = coms.get_json_cfg('../cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    upload_filename = debug_filename

    local_file = 'tmp/' + upload_filename

    nod = js[nodename]
    remoteip = nod['ip']
    if isinstance(remoteip, list):
        remoteip = remoteip[index]

    boardusr = nod['usr']
    boardpass = nod['pw']


    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if force_file == '':
        remote_file = '/tmp/' + upload_filename
        dat = await ftpdl.ftp_get_file(ftpip, ftpcwd, ftpusr, ftppass, upload_filename)
        name = ''
        with tempfile.NamedTemporaryFile('wb',delete=False) as f:
            name = f.name
            f.write(dat.getbuffer())
        await scpul.scp_upload(remoteip, name, remote_file, boardusr, boardpass)
        os.unlink(name)
    else:
        remote_file = force_file
        #upload update file
        await scpul.scp_upload(remoteip, force_file, remote_file, boardusr, boardpass)

    # execline.execlines(remoteip, boardusr, boardpass)

    updatefirmware.rebootcmd(remoteip, boardusr, boardpass)

def update_rtos(nodename, force_file='', index=0):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    t = loop.create_task(_update_rtos(nodename, force_file, index))
    loop.run_until_complete(t)
    
    os.system("pause")
