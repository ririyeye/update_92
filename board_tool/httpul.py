import os
from unittest import result
import asyncssh
import aiohttp
import random
from aiohttp import web
from .execline import *
from .comms import *


class httpuls(object):
    def __init__(
        self,
        conn: asyncssh.SSHClientConnection,
        fname: str,
        remotename: str = "/tmp/update",
    ):
        self.fname = fname
        self.conn = conn
        self.remotename = remotename

    async def handle(self, request):
        name = request.match_info.get("name", "Anonymous")
        wf = web.FileResponse(path=self.fname)
        return wf

    async def runweb(self) -> int:
        app = web.Application()
        app.add_routes(
            [web.get("/", self.handle), web.get("/{name}", self.handle)]
        )

        self.runner = web.AppRunner(app)
        await self.runner.setup()
        for i in range(10):
            port = random.randint(40000, 45000)
            try:
                self.site = web.TCPSite(self.runner, "0.0.0.0", port=port)
                await self.site.start()
                print("start ok!! , port = {0}".format(port))
                return port
            except OSError as e:
                print("bind error , port = {0}".format(port))

        raise

    async def tryupload(self):
        port = await self.runweb()
        await self.conn.run("cd /tmp;ls /tmp")
        localaddr = self.conn._local_addr
        cmd = "wget http://{0}:{1}/123 -O {2}".format(
            localaddr, port, self.remotename
        )
        result = await self.conn.run(cmd)
        await self.site.stop()
        await self.runner.shutdown()


async def httpulfile(
    conn: asyncssh.SSHClientConnection, localfile: str, remotefile: str
):
    localmd5 = get_file_md5(localfile)
    h = httpuls(conn, localfile, remotefile)
    await h.tryupload()
    ret = await execlines(conn, "md5sum " + remotefile)
    getmd5 = ret.split(" ")[0]
    if localmd5 != getmd5:
        print("download fail !!!")
        return True
    return False


async def httpulfile_shell(
    ip: str,
    port: str,
    username: str,
    password: str,
    localfile: str,
    remotefile: str,
):
    async with asyncssh.connect(
        host=ip,
        port=port,
        username=username,
        password=password,
        known_hosts=None,
        config=None,
        server_host_key_algs=["ssh-rsa"],
    ) as conn:
        await httpulfile(conn, localfile, remotefile)

async def httpulfile_shell_wdt(
    ip: str,
    port: str,
    username: str,
    password: str,
    localfile: str,
    remotefile: str,
):
    async with asyncssh.connect(
        host=ip,
        port=port,
        username=username,
        password=password,
        known_hosts=None,
        config=None,
        server_host_key_algs=["ssh-rsa"],
    ) as conn:
        await httpulfile(conn, localfile, remotefile)
        await execlines(conn,"chmod 777 " + remotefile)


def httpulfile_sync(
    ip: str,
    port,
    username: str,
    password: str,
    localfile: str,
    remotefile: str,
):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        httpulfile_shell(ip, port, username, password, localfile, remotefile)
    )


def httpulfile_sync_wdt(
    ip: str,
    port,
    username: str,
    password: str
):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(
        httpulfile_shell_wdt(
            ip,
            port,
            username,
            password,
            os.path.join(os.path.dirname(__file__), "ar_wdt_service"),
            "/tmp/ar_wdt_service2",
        )
    )
