import winsize

class WatchWinsize:
    def __init__(self, p):
        self.__p = p
        winsize.add_proc(p)

    def close(self):
        winsize.remove_proc(p)

