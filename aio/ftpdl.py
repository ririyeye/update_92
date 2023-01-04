#!/usr/bin/python3

import aioftp
import asyncio
import os
import io
import aioftp.errors


async def getsz(client, filename) -> int:
    try:
        code, info = await client.command("SIZE " + filename, "2xx")
        return int(info[0].lstrip())
    except aioftp.errors.StatusCodeError as e:
        if not e.received_codes[-1].matches("50x"):
            raise


async def ftp_get_file(host: str, cwd: str, usr, password, filename: str, datacallback=None) -> io.BytesIO:
    async with aioftp.Client.context(host, 21, usr, password) as client:
        await client.change_directory(cwd)
        try:
            ftpsize = await getsz(client, filename)
            stream = await client.download_stream(filename)
        except aioftp.errors.StatusCodeError as e:
            print("download error :" + str(e))
            return None

        tmp = io.BytesIO()
        download_size = 0

        print("download " + filename)
        async for block in stream.iter_by_block(1024 * 128):
            if datacallback:
                await datacallback(block, download_size)
            download_size = download_size + len(block)
            txt = format(download_size / ftpsize * 100, '.2f') + '%'
            print('\r---' + txt, end="")
            tmp.write(block)

        print('\n')
        print("download ok!")
        return tmp


class savehelper(object):

    def __init__(self, in_f):
        self.f = in_f
        self.q = asyncio.Queue(maxsize=100)
        self.stask = asyncio.create_task(self.savetask())
        self.runflg = True

    async def savetask(self):
        while True:
            item = await self.q.get()

            if item is None:
                self.q.task_done()
                return
            data = item[0]
            offset = item[1]

            self.f.seek(offset)
            self.f.write(data)
            self.q.task_done()

    async def callback(self, data, offset):
        await self.q.put((data, offset))

    async def wait_exit(self):
        await self.q.put(None)
        await self.q.join()
        await self.stask
        pass

async def ftp_dl_file(host: str, cwd: str, usr, password, filename: str, localfile: str):
    with open(localfile, 'wb') as f:
        s = savehelper(f)
        await ftp_get_file(host, cwd, usr, password, filename, datacallback=s.callback)
        await s.wait_exit()
        pass


if __name__ == "__main__":
    from coms import get_json_cfg
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # filename = "a7_rtos.nonsec.img"
    filename = "sdk-artosyn-videowave-1.0.1.5.tar.gz"
    js = get_json_cfg('../cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    ret = loop.run_until_complete(ftp_get_file(host=ftpip, cwd=ftpcwd, usr=ftpusr, password=ftppass, filename=filename))
    if ret is not None:
        with open(filename, 'wb') as f:
            ret.seek(0)
            f.write(ret.getbuffer())
        print('download ok!')
    else:
        print('download error!')

    os.system("pause")