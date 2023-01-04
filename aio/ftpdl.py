#!/usr/bin/python3

import aioftp
import asyncio
import os
import json
import io
import aioftp.errors
import asyncssh
import coms

async def getsz(client, filename) -> int:
    try:
        code, info = await client.command("SIZE " + filename, "2xx")
        return int(info[0].lstrip())
    except aioftp.errors.StatusCodeError as e:
        if not e.received_codes[-1].matches("50x"):
            raise


async def get_file(filename: str, host: str, usr, password, cwd) -> io.BytesIO:
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
            download_size = download_size + len(block)
            txt = format(download_size / ftpsize * 100, '.2f') + '%'
            print('\r---' + txt, end="")
            tmp.write(block)
        print('\n')
        print("download ok!")
        return tmp





if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # filename = "a7_rtos.nonsec.img"
    filename = "sdk-artosyn-videowave-1.0.1.5.tar.gz"
    js = coms.get_json_cfg('../cfg.json')
    ftpcfg = js['ftp']

    ftpip = ftpcfg['ip']
    ftpcwd = ftpcfg['workpath']
    ftpusr = ftpcfg['usr']
    ftppass = ftpcfg['pw']

    ret = loop.run_until_complete(get_file(filename, host=ftpip, usr=ftpusr, password=ftppass, cwd=ftpcwd))
    if ret is not None:
        with open(filename, 'wb') as f:
            ret.seek(0)
            f.write(ret.getbuffer())
        print('download ok!')
    else:
        print('download error!')

    os.system("pause")