from aiohttp import web
import asyncio
import os
import asyncssh
import random
import io


async def execlines(conn: asyncssh.SSHClientConnection, lines: str, showlines=False) -> str:
    async with conn.create_process(
            "#!/bin/sh \n "
            "export LD_LIBRARY_PATH=/lib:/usr/lib:/local/lib:/local/usr/lib:$LD_LIBRARY_PATH \n"
            "export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/local/bin/:/local/usr/bin/:/local/usr/sbin:$PATH \n" + lines +
            "\n") as process:
        with io.StringIO() as outline:
            async for line in process.stdout:
                outline.write(line)
                if showlines == True:
                    print(line)

            return outline.getvalue()

async def testdexecl():
    async with asyncssh.connect('192.168.10.104',
                                username='root',
                                password='artosyn',
                                known_hosts=None,
                                server_host_key_algs=['ssh-rsa']) as conn:
        lines = await execlines(conn=conn, lines="cat /tmp/123")
        pass


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(testdexecl())

    os.system("pause")
