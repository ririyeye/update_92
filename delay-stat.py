#!/usr/bin/python3

import os
import stat
import updateonce
import json
import sys
import re


class comlog:
    def __init__(self, time: str, thread: str,  level: str, label: str, fun: str, comment: str, log: str) -> None:
        self.time = time
        self.thread = thread
        self.level = level
        self.label = label
        self.fun = fun
        self.comment = comment
        self.log = log

def regexlog(str0):
    pat = re.compile(
        "\\[(\\d+\\.\\d+)\\] \\[(\\w+)\\] \\[(\\w+)\\] \\[([\\w-]+)\\] (\\w+):(.*)")
    out = []
    for match in pat.finditer(str0):
        g0 = match.group(0)
        time = match.group(1)
        thread = match.group(2)
        level = match.group(3)
        label = match.group(4)
        fun = match.group(5)
        comment = match.group(6)
        c0 = comlog(time, thread, level, label, fun, comment, g0)
        out.append(c0)
    return out

def clientproc(clientgrp : list[comlog]):
    start = re.compile("send start = (\\d+)")
    end = re.compile("send end = (\\d+)")

    startdict = {}
    enddict = {}

    for clilog in clientgrp:
        s0 = start.search(clilog.log)
        if s0 is not None:
            pos = int(s0.group(1))
            startdict[pos] = clilog
        e0 = end.search(clilog.log)
        if e0 is not None:
            pos = int(e0.group(1))
            enddict[pos] = clilog

    return startdict, enddict

def daemonproc(daemongrp : list[comlog]):
    recv = re.compile("rpc recv len = (0(?:x\\w+)),cur = (0(?:x\\w+)) , max = (0(?:x\\w+))")
    start = re.compile("tx pos = (0(?:x\\w+))")

    txdict = {}
    recvdict = {}

    for daelog in daemongrp:
        # tcp recv
        r0 = recv.search(daelog.log)
        if r0 is not None:
            pos = int(r0.group(2),16)
            if pos not in recvdict:
                recvdict[pos] = daelog

        # tx 选择第一次
        s0 = start.search(daelog.log)
        if s0 is not None:
            pos = int(s0.group(1),16)
            if pos not in txdict:
                txdict[pos] = daelog

    return recvdict, txdict

if __name__ == "__main__":
    clientgrp = []
    with open("client.txt", 'r') as f0:
        str0 = f0.read()
        clientgrp = regexlog(str0)

    start , end = clientproc(clientgrp)

    with open("daemon.txt", 'r') as f0:
        str0 = f0.read()
        daemongrp = regexlog(str0)

    recvdict , txdict = daemonproc(daemongrp)
    
    difflist = {}
    num = 0
    allval = 0
    with open("out.txt" , 'w') as out:
        out.truncate()
        for pos in start:
            if pos in recvdict:
                tdiff = float(recvdict[pos].time) - float(start[pos].time)
                tdiff = tdiff * 1000000
                out.write(str(tdiff) + "\n")
                
                intval = int(tdiff / 5)
                if intval not in difflist:
                    difflist[intval] = 0
                difflist[intval] = difflist[intval] + 1
                num = num + 1
                allval  = allval + tdiff

    for inttim in sorted(difflist):
        print(inttim * 5, difflist[inttim] , '{:.2%}'.format(difflist[inttim] / num))
    
    print("avg =" , allval / num)
