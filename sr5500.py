#!/usr/bin/python3

import asyncio

async def tcp_echo_client(message):

    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 6002)

    await reader.readuntil('\r\nSR5500> '.encode())

    for txt in message:
        print(f'Send: {txt!r}')
        writer.write(txt.encode())
        await writer.drain()
        await reader.readuntil('\r\n'.encode())
        ret = await reader.readuntil('\r\n'.encode())
        print('get dat' , ret.decode())
        await reader.readuntil('\rSR5500> '.encode())

    await asyncio.sleep(1000)

if __name__ == "__main__":
    asyncio.run(tcp_echo_client([
        ':*IDN?\r',
        ':*OPC?\r',
        ':*OPT?\r',
        # ':CHAN1:PATH1:DELay 10\r',
        # ':CHAN1:PATH1:MODE FIXed\r'
        ':CHAN1:PATH1:DELay?\r',
        ':BAND\r',
    ]))
    print(123)
