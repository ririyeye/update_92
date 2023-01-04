import asyncio
from random import SystemRandom
import asyncssh
from typing import List
from socket import error as socket_error
import errno
from datetime import datetime, timedelta
import os


class ssh_scanner(object):

    def __init__(self, ips, ports, configs) -> None:
        self.ips = ips
        self.ports = ports
        self.configs = configs

        self.output = []

    async def trysshconnect(self, ip, port, config: dict):
        try:
            lefttime = self.timeoutpoint - datetime.now()
            leftsecond = lefttime.total_seconds()

            conn = asyncssh.connect(host=ip,
                                    port=port,
                                    username=config['username'],
                                    password=config['password'],
                                    known_hosts=None,
                                    server_host_key_algs=['ssh-rsa'])
            ret = await asyncio.wait_for(conn, timeout=leftsecond)
            print("{}:{} ssh Connected".format(ip, port))
            self.output.append((ip, port, config))
            return
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            pass

        lefttime = self.timeoutpoint - datetime.now()
        leftsecond = lefttime.total_seconds()
        await asyncio.sleep(leftsecond)

    async def scanner(self, ip, port, configs: list[dict]):
        lefttime = self.timeoutpoint - datetime.now()
        leftsecond = lefttime.total_seconds()

        fut = asyncio.open_connection(ip, port)
        try:
            reader, writer = await asyncio.wait_for(fut, timeout=leftsecond)
            print("{}:{} port Connected".format(ip, port))

            tasks = [asyncio.create_task(self.trysshconnect(ip, port, config)) for config in configs]

            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in tasks:
                if not task.done():
                    task.cancel()
            self.port_res.cancel()
            return

        except asyncio.TimeoutError:
            pass
        except socket_error as serr:
            if serr.errno != errno.EINVAL:
                print('Error {}:{} {}'.format(ip, port, serr))
            pass
        except Exception as exc:
            print('Error {}:{} {}'.format(ip, port, exc))
            pass

    async def sshscan(self, timeout: int) -> list[(str, str, dict)]:
        self.output = []
        self.timeoutpoint = datetime.now() + timedelta(seconds=timeout)

        tasks = [asyncio.create_task(self.scanner(ip, port, configs)) for port in self.ports for ip in self.ips]

        self.port_res = asyncio.gather(*tasks)
        try:
            await asyncio.wait_for(self.port_res, timeout=timeout)
        except asyncio.TimeoutError:
            pass
        except asyncio.CancelledError:
            pass

        return self.output


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    configs = [{'username': 'root', 'password': 'artosyn'}]

    ips = ["192.168.10.{}".format(i) for i in range(1, 255)]
    ports = [22, 80, 443, 8080]
    timeout = 20
    s = ssh_scanner(ips, ports, configs)
    results = loop.run_until_complete(s.sshscan(timeout))
    for res in results:
        print("{}:{} [{}:{}] is ok!".format(res[0], res[1], res[2]['username'], res[2]['password']))
    os.system("pause")
