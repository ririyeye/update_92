# examples/server_simple.py
from aiohttp import web
import os
import asyncio
import asyncssh


class scpdls(object):

    def __init__(self, conn: asyncssh.SSHClientConnection, fname: str, remotename: str = '/tmp/update'):
        self.fname = fname
        self.conn = conn
        self.remotename = remotename

    async def tryupload(self):

        def cb(local_file, remote_file, sent, total):
            percent = format(sent / total * 100, '.2f') + '%'
            print("\rcopy ", local_file, percent, end="")

        await asyncssh.scp(self.fname, (self.conn, self.remotename), progress_handler=cb)
        print('\n')


async def testupload():
    async with asyncssh.connect('192.168.10.104',
                                username='root',
                                password='artosyn',
                                known_hosts=None,
                                server_host_key_algs=['ssh-rsa']) as conn:
        hd = scpdls(conn=conn, fname='sdk/a7_rtos.nonsec.img', remotename='/tmp/ppp')
        await hd.tryupload()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(testupload())

    os.system("pause")