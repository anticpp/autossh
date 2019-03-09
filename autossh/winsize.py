#!/usr/bin/env python

import os
import sys
import struct
import signal
import fcntl
import termios

## Process to be watched.
__procs = {}

def auto():
    signal.signal(signal.SIGWINCH, __sigwinch)

## Add process to be auto winsize
## Input:
##   p pexpect.Spwan, a pexpect spwan process
def add_proc(p):
    ## Add to watch list
    __procs[p.pid] = p

    ## Init winsize
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ , s))
    p.setwinsize(a[0], a[1])

## Remove process
def remove_proc(p):
    del __procs[p.pid]

## Handle signal.SIGWINCH
def __sigwinch(sig, data):
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ , s))
    for pid in __procs:
        __procs[pid].setwinsize(a[0], a[1])
    return None   


