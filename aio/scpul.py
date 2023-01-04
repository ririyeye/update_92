# examples/server_simple.py
from aiohttp import web
import os
import asyncio
import asyncssh


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(scp_upload())

    os.system("pause")