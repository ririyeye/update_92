# examples/server_simple.py
from aiohttp import web
import os
import asyncio
import asyncssh

class httptool(object):

    def __init__(self, fname: str):
        self.fname = fname

    async def handle(self, request):
        name = request.match_info.get('name', "Anonymous")
        wf = web.FileResponse(path=self.fname)
        return wf

    async def runweb(self,port = 50000):
        app = web.Application()
        app.add_routes([web.get('/', self.handle), web.get('/{name}', self.handle)])

        self.runner = web.AppRunner(app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, "0.0.0.0", port=port)
        await self.site.start()
        print("start ok!!")


async def trydownload(tool: httptool):
    async with asyncssh.connect('192.168.10.104',
                                username='root',
                                password='artosyn',
                                known_hosts=None,
                                server_host_key_algs=['ssh-rsa']) as conn:
        print('connect ok!')
        await conn.run("cd /tmp;ls /tmp")
        result = await conn.run("wget http://192.168.10.102:50000/123 -O /tmp/123")
        await tools.site.stop()
        # await tool.runner.shutdown()
        pass
    


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tools = httptool('test.py')
    loop.run_until_complete(tools.runweb())
    loop.create_task(trydownload(tools))


    loop.run_forever()

    os.system("pause")