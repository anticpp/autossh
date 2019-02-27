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

    def settimeout(self, s):
        self.__timeout = s

    ## Input
    ##  - info tupple("host", "user", "password"), hostinfo
    ##  - expects array[string], user expects for extention
    ##  - reacts array[string], reacts for user expects
    ## Return
    ##  - result bool
    ##  - errmsg string
    def login(self, info, expects=None, reacts=None):
        ok = True
        errmsg = ""
        host = info[0]
        user = info[1]
        password = info[2]
        
        default_expects = ["yes/no", "assword:", "[#\$]", pexpect.TIMEOUT, pexpect.EOF]
        if expects is None:
            expects = default_expects
        else:
            expects = default_expects + expects

	self.__child = pexpect.spawn("ssh", ["%s@%s"%(user, host)])
        self.__child.logfile_read = sys.stdout
        while True:
            n = self.__child.expect(expects, timeout=self.__timeout)
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
            else:      # user expects
                self.__child.sendline(reacts[n-len(default_expects)])
        return ok, errmsg
    
    ## WHY:
    ##  There are some situations which for secure reason, 
    ##  you have to jump from a secure node to target machine.
    ##
    ## Input
    ##  - info tupple("host", "user", "password"), jump target hostinfo
    ## Return
    ##  - result bool
    ##  - errmsg string
    def jump(self, info):
        ok = True
        errmsg = ""
        host = info[0]
        user = info[1]
        password = info[2]

        self.__child.sendline("ssh %s@%s"%(user, host))
        while True:
            n = self.__child.expect(["yes/no", "assword:", pexpect.TIMEOUT, pexpect.EOF], timeout=self.__timeout)
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

