import os
import sys
import pexpect
import yaml
from . import config
from . import lookup
from . import winsize

# Set config file path, or using default.
def set_config(path):
    config.set_path(path)

def new(target):
    s = SSH(target)
    return s

class SSH:
    def __init__(self, target):
        self.__target = target
        self.__child = None
        self.__timeout = 20
        self.__wd = None
        self.__c = config.load()
        self.__lu = lookup.load(os.path.expanduser(self.__c.host_file))

    def close(self):
        if self.__child is None:
            return 

        if self.__wd is not None:
            self.__wd.close()
            self.__wd = None

        self.__child.close()
        self.__child = None

    def settimeout(self, s):
        self.__timeout = s

    ## Set auto window size
    def autowinsize(self):
        if self.__wd is None:
            self.__wd = winsize.WatchDog(self.__child)

    ## Input
    ##  - expects array[string], user expects for extention
    ##  - reacts array[string], reacts for user expects
    ## Return
    ##  - result bool
    ##  - errmsg string
    def login(self, expects=None, reacts=None):
        ok = True
        errmsg = ""

        ok, info = self.__lu.get(self.__target)
        if not ok:
            return False, "Host not found '%s'."%(self.__target)

        host = info[0]
        port = info[1]
        user = info[2]
        password = info[3]
        
        default_expects = ["yes/no", "assword:", "[#\$]", pexpect.TIMEOUT, pexpect.EOF]
        if expects is None:
            expects = default_expects
        else:
            expects = default_expects + expects

        if port==0:
            self.__child = pexpect.spawn("ssh", ["%s@%s"%(user, host)])
        else:
            self.__child = pexpect.spawn("ssh", ["%s@%s"%(user, host), "-p", port])
        self.__child.logfile_read = sys.stdout.buffer
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
    ##  There are some situations, etc. for secure reason, 
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
        port = info[1]
        user = info[2]
        password = info[3]

        self.__child.sendline("ssh -p %s %s@%s -p %s"%(port, user, host))
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

        return ok, errmsg

    ## Function
    ##    Send local file to remote.
    ## Input
    ##  - src string, Local source file
    ##  - dst string, Remote destination
    ## Return
    ##  - result bool
    ##  - errmsg string
    def send_file(self, src, dst):
        ok = True
        errmsg = ""

        ok, info = self.__lu.get(self.__target)
        if not ok:
            return False, "Host not found '%s'."%(self.__target)

        host = info[0]
        port = info[1]
        user = info[2]
        password = info[3]

        if port==0:
            self.__child = pexpect.spawn("scp", [src, "%s@%s:%s"%(user, host, dst)])
        else:
            self.__child = pexpect.spawn("scp", [src, "-p", port, "%s@%s:%s"%(user, host, dst)])

        self.__child.logfile_read = sys.stdout.buffer
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

    ## Function
    ##    Pull remote file to local.
    ## Input
    ##  - src string, Remote source file
    ##  - dst string, Local destination
    ## Return
    ##  - result bool
    ##  - errmsg string
    def pull_file(self, src, dst):
        ok = True
        errmsg = ""

        ok, info = self.__lu.get(self.__target)
        if not ok:
            return False, "Host not found '%s'."%(self.__target)

        host = info[0]
        port = info[1]
        user = info[2]
        password = info[3]
    
        if port==0:
            self.__child = pexpect.spawn("scp", ["%s@%s:%s"%(user, host, src), dst])
        else:
            self.__child = pexpect.spawn("scp", ["-p", port, "%s@%s:%s"%(user, host, src), dst])
        self.__child.logfile_read = sys.stdout.buffer
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
        ## Close logfile_read before interact.
        self.__child.logfile_read = None

        ## The default escape character is `\x1d`(Ctrl+]),
        ## which conflicts with vim.
        ## Set to None to disable escaping from child.
        self.__child.interact(escape_character=None)

