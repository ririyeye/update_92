from aiohttp import web
import asyncio
import os
import asyncssh
import random
from .coms import get_json_cfg

class httpuls(object):

    def __init__(self, conn: asyncssh.SSHClientConnection, fname: str, remotename: str = '/tmp/update'):
        self.fname = fname
        self.conn = conn
        self.remotename = remotename

    async def handle(self, request):
        name = request.match_info.get('name', "Anonymous")
        wf = web.FileResponse(path=self.fname)
        return wf

    async def runweb(self) -> int:
        app = web.Application()
        app.add_routes([web.get('/', self.handle), web.get('/{name}', self.handle)])

        self.runner = web.AppRunner(app)
        await self.runner.setup()
        for i in range(10):
            port = random.randint(10000, 20000)
            try:
                self.site = web.TCPSite(self.runner, "0.0.0.0", port=port)
                await self.site.start()
                print("start ok!! , port = {0}".format(port))
                return port
            except OSError as e:
                print("bind error , port = {0}".format(port))
                if i == 9:
                    raise

    async def tryupload(self):
        port = await self.runweb()
        await self.conn.run("cd /tmp;ls /tmp")
        localaddr = self.conn._local_addr
        cmd = "wget http://{0}:{1}/123 -O {2}".format(localaddr, port, self.remotename)
        result = await self.conn.run(cmd)
        await self.site.stop()
        await self.runner.shutdown()

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


async def scp_upload(remoteip, local_file, remote_file, usr, pwd):
    async with asyncssh.connect(remoteip,
                                username=usr,
                                password=pwd,
                                known_hosts=None,
                                server_host_key_algs=['ssh-rsa']) as conn:
        hd = scpdls(conn=conn, fname=local_file, remotename=remote_file)
        await hd.tryupload()





async def testupload():
    async with asyncssh.connect('192.168.10.104',
                                username='root',
                                password='artosyn',
                                known_hosts=None,
                                server_host_key_algs=['ssh-rsa']) as conn:
        hd = httpuls(conn=conn, fname='cfg.json')
        await hd.tryupload()


if __name__ == "__main__":

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

    loop.run_until_complete(testupload())

    os.system("pause")
