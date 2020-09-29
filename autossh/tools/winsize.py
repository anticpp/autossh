#!/usr/bin/env python

import os
import sys
import struct
import signal
import fcntl
import termios

## Process to be watched.
__procs = {}

## Handle signal.SIGWINCH
def __sigwinch(sig, data):
    for pid in __procs:
        auto_adjust(__procs[pid])

def add_proc(p):
    __procs[p.pid] = p

def remove_proc(p):
    del __procs[p.pid]

def auto_adjust(p):
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ , s))
    p.setwinsize(a[0], a[1])

signal.signal(signal.SIGWINCH, __sigwinch)

##
## wd = WatchDog(proc)
## /* Windows size of `proc` will be re-adjust automatically. */
## ...
## wd.close()
##
class WatchDog:
    def __init__(self, p):
        self.__p = p
        add_proc(p)
        auto_adjust(p)

    def close(self):
        remove_proc(self.__p)

