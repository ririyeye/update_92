import re
from time import sleep
from turtle import xcor
import matplotlib
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import os
from matplotlib.widgets import Button, RadioButtons, CheckButtons


class pctool_dat:
    time: list[int]
    fchlock: int
    slotlock: int
    slotgain: list[int]
    ldpc_err: int
    snr: int

    def __init__(self, match: re.Match[str]) -> None:
        self.time = [
            int(match.group(1)),
            int(match.group(2)),
        ]
        self.fchlock = int(match.group(3)) * 20 + 20
        self.slotlock = int(match.group(4))
        self.slotgain = [
            int(match.group(5)),
            int(match.group(6)),
            int(match.group(7)),
            int(match.group(8)),
        ]
        self.ldpc_err = int(match.group(9)) * 20 + 60
        self.snr = int(match.group(10))

    def get_dat(self) -> list[int]:
        return [
            self.fchlock,
            self.slotlock,
            self.slotgain[0],
            self.slotgain[1],
            self.slotgain[2],
            self.slotgain[3],
            self.ldpc_err,
            self.snr,
        ]


def taketime(elem: pctool_dat):
    return int(elem.time[0])


def regexproc(gnd) -> list[pctool_dat]:
    exp = r"^\[(\d+)\]\[\w+\]\[\w+\] \[(\d+)\] bb_update_osd_info fch lock (\d), slot lock (\d), slot agc\[\d\](\d+), \[\d\](\d+), \[\d\](\d+), \[\d\](\d+), ldpc err (\d), snr (\d+)"
    pat = re.compile(exp, re.MULTILINE)
    timlist = []

    for match in pat.finditer(gnd):
        p = pctool_dat(match)
        timlist.append(p)

    timlist.sort(key=taketime)
    return timlist


import numpy as np


class plot_ctrl:
    labstr = [
        'fchlock',
        'slotlock',
        'slotgain0',
        'slotgain1',
        'slotgain2',
        'slotgain3',
        'ldpc_err',
        'snr',
    ]

    labelmask = [
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
    ]
    lines: list[Line2D]

    def __init__(self, lines: list[Line2D], fig):
        self.lines = lines
        self.fig = fig

    def func(self, label):
        index = self.labstr.index(label)
        self.lines[index].set_visible(not self.lines[index].get_visible())
        self.fig.canvas.draw()


def plot_pctooldat(dat: list[pctool_dat]) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    t = [test.time[0] / 1000 for test in dat]
    dats = [test.get_dat() for test in dat]

    ax.ticklabel_format(useOffset=False, style='plain')

    pt = ax.plot(t, dats, 'r-')
    pt[0].set_color('green')
    pt[1].set_color('blue')
    pt[2].set_color('black')
    pt[3].set_color('purple')
    pt[4].set_color('red')
    pt[5].set_color('yellow')
    pt[6].set_color('gray')
    pt[7].set_color('Aqua')

    ctrl = plot_ctrl(pt, fig)

    ax_check = plt.axes((0.8, 0.001, 0.2, 0.3))
    plot_button = CheckButtons(ax_check, ctrl.labstr, ctrl.labelmask)
    plot_button.on_clicked(ctrl.func)

    plt.show()


if __name__ == "__main__":
    with open("out.txt", 'r') as f0:
        gnd = f0.read()
        outdat = regexproc(gnd)
        plot_pctooldat(outdat)
