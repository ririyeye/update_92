#!/usr/bin/python3

import asyncio, asyncssh, sys
import ssl
import os
import aioconsole


class ssl_test(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_ctx.options |= ssl.OP_NO_TLSv1
        self.ssl_ctx.options |= ssl.OP_NO_TLSv1_1
        self.ssl_ctx.load_cert_chain('client/pri.ca', keyfile='client/pri_key.pem', password="12138")
        self.ssl_ctx.load_verify_locations(cafile='ca/ca.cer')
        self.ssl_ctx.check_hostname = False
        self.ssl_ctx.verify_mode = ssl.VerifyMode.CERT_REQUIRED
        # ssl_ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
        self._in = ssl.MemoryBIO()
        self._out = ssl.MemoryBIO()
        self._ssl_sock = self.ssl_ctx.wrap_bio(self._in, self._out, server_side=False)

    async def handshake(self):
        self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)

        while True:
            try:
                self._ssl_sock.do_handshake()
                break
            except ssl.SSLWantReadError:
                self.writer.write(self._out.read())
                data = await self.reader.read(1024)
                self._in.write(data)

        while True:
            wr = self._out.read()
            lens = len(wr)
            if lens > 0:
                self.writer.write(wr)
                await self.writer.drain()
            else:
                break
        print("shake hand ok!")

    async def read_task(self):
        while True:
            data = await self.reader.read(1024)
            self._in.write(data)
            try:
                rd = self._ssl_sock.read()
                lens = len(rd)
                print(rd)
            except ssl.SSLWantReadError:
                pass

    async def read_input(self):
        while True:
            var = await aioconsole.ainput('please input data')
            bytes = str.encode(var)

            num = self._ssl_sock.write(bytes)
            if num > 0:
                self.writer.write(self._out.read())

    async def echo_client(self):
        await self.handshake()

        asyncio.create_task(self.read_task())
        asyncio.create_task(self.read_input())

        await asyncio.sleep(30000)


if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()
    ts = ssl_test('192.168.30.198', 8888)
    async_loop.run_until_complete(ts.echo_client())
    async_loop.close()
    os.system("pause")
