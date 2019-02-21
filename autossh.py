#!/usr/bin/env python

import sys
import pexpect

class AutoSSH:
    def __init__(self):
        self.__child = None
        self.__timeout = 3

    def close(self):
        if self.__child is None:
            return 
	self.__child.close()
        self.__child = None

    def settimeout(s):
        self.__timeout = s

    ## Input
    ##  - info tupple("host", "user", "password"), hostinfo
    ## Return
    ##  - result bool
    ##  - errmsg string
    def login(self, info):
        ok = True
        errmsg = ""
        host = info[0]
        user = info[1]
        password = info[2]

	self.__child = pexpect.spawn("ssh", ["%s@%s"%(user, host)])
        self.__child.logfile_read = sys.stdout
        while True:
            n = self.__child.expect(["yes/no", "assword:", "[#\$]", pexpect.TIMEOUT, pexpect.EOF], timeout=self.__timeout)
            if n==0:   # yes/no
                self.__child.sendline("yes")
            elif n==1: # assword:
                self.__child.sendline(password)
            elif n==2: # [#\$]
                break
            elif n==3: # TIMEOUT
                ok = False
                errmsg = "TIMEOUT"
                break;
            elif n==4: # EOF
                ok = False
                errmsg = "EOF"
                break;
            else:
                ok = False
                errmsg = "unknown"
        return ok, errmsg

    ## Input
    ##  - info tupple("host", "user", "password"), hostinfo
    ##  - src string, source file
    ##  - dst string, destination
    ## Return
    ##  - result bool
    ##  - errmsg string
    def scp(self, info, src, dst):
        ok = True
        errmsg = ""
        host = info[0]
        user = info[1]
        password = info[2]

        self.__child = pexpect.spawn("scp", [src, "%s@%s:%s"%(user, host, dst)])
        self.__child.logfile_read = sys.stdout
        while True:
            n = self.__child.expect(["yes/no", "assword:", pexpect.TIMEOUT, pexpect.EOF], timeout=self.__timeout)
            if n==0:   # yes/no
                self.__child.sendline("yes")
            elif n==1: # assword:
                self.__child.sendline(password)
            elif n==2: # TIMEOUT
                ok = False
                errmsg = "TIMEOUT"
            else:      # EOF
                ## TODO:
                ## Can not distinguish error or success with EOF
                ## For example, if scp error causing by network or invalid password,
                ## the child will print error message and EOF.
                break
        return ok, errmsg

    def exit(self):
	self.__child.sendline("exit")

    def interact(self):
        self.__child.interact()

