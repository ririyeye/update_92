import asyncio
from datetime import datetime
import os
import pathlib
from typing import Callable
import aioftp
import re
import aiofiles


def parse_list(b):
    reglist = re.compile(
        r'(\d+-\d+-\d+ *\d+:\d+[A-Z]+) *(\d+|(?:<DIR>)) *(\w.*)')

    # '06-08-23  05:32PM       <DIR>          data'
    # '09-13-23  05:48PM                 2239 1.txt'
    line = b.decode('UTF-8').rstrip("\r\n")
    m = reglist.search(line)
    assert m is not None
    info = {}
    info["modify"] = datetime.strptime(m.group(1), '%m-%d-%y %I:%M%p')
    if m.group(2) == '<DIR>':
        info["type"] = 'dir'
    else:
        info["type"] = 'file'
        info["size"] = int(m.group(2))

    info["name"] = m.group(3)

    return pathlib.PurePosixPath(m.group(3)), info


class filesync:

    def __init__(self, lk, f, offset, data):
        self.lk = lk
        self.f = f
        self.offset = offset
        self.data = data

    async def writer(self):
        async with self.lk:
            await self.f.seek(self.offset)
            await self.f.write(self.data)


async def ftp_download_file(client: aioftp.Client, serverpath, info, localpath,
                            dl_index = -1):
    async with aiofiles.open(os.path.join(localpath, info['name']),
                             mode='wb') as f:
        lk = asyncio.Lock()
        stream = await client.download_stream(serverpath)
        async with asyncio.TaskGroup() as tg:
            offset = 0
            async for block in stream.iter_by_block(128 * 1024):
                # if dl_index >= 0:
                #     stdscr

                syn = filesync(lk, f, offset, block)
                offset = offset + len(block)
                tg.create_task(syn.writer())
        await stream.finish()


class dl_group():

    def __init__(self, max=10):
        self.sem = asyncio.Semaphore(max)
        self.index = -1

    async def create_download(self, remoteip, usr, password, cwd, name, info,
                              localpath):
        async with self.sem:
            async with aioftp.Client.context(host=remoteip,
                                             user=usr,
                                             password=password) as dl:
                await dl.change_directory(cwd)
                self.index = self.index + 1
                await ftp_download_file(dl, name, info, localpath, self.index)


async def ftpdownload_async(
        remoteip, cwd, usr, password,
        serverparten: Callable[[pathlib.PurePosixPath, list[str]],
                               bool], localpath):
    dl = dl_group(5)

    async with asyncio.TaskGroup() as tg:
        async with aioftp.Client.context(
                host=remoteip,
                user=usr,
                password=password,
                parse_list_line_custom=parse_list,
                parse_list_line_custom_first=True) as client:
            await client.change_directory(cwd)

            for name, info in (await client.list()):
                if not serverparten(name, info):
                    continue
                tg.create_task(
                    dl.create_download(remoteip, usr, password, cwd, name,
                                       info, localpath))
