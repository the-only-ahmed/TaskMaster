#!/usr/bin/env python
import os
import sys
import os.path
import atexit
import readline
import rlcompleter
import logger
import signal
import threading
import time

from shell import *
from programList import ProgramList

interf = None
progs_lock = None
progs = None

def signal_handler(signal, frame):
    if interf:
        interf.quit()
    exitP(progs)

def thread_check_progs():
    """
    Function executed in the thread for checking the state of
    all the progs
    """
    while True:
        try:
            progs_lock.acquire(True)
            progs.check()
            progs_lock.release()
            time.sleep(0.01)
        except:
            exit()

def check_fileExistance():
    if os.path.exists(historyPath):
        readline.read_history_file(historyPath)
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        if os.access(sys.argv[1], os.R_OK):
            fd = open(sys.argv[1], 'r')
            return fd
        else:
            print("File can't be opened")
            logger.log("File can't be opened")
            exit()
    else:
        print("File doesn't exist")
        logger.log("File doesn't exist")
        exit()

def main():
    print "BEGIN TASKMASTER"
    logger.log("BEGIN TASKMASTER")
    signal.signal(signal.SIGINT, signal_handler)
    fd = check_fileExistance()

    global progs
    progs = ProgramList(fd)
    progs.launch()

    global progs_lock
    progs_lock = threading.Lock()

    # launch a thread to test progs
    t = threading.Thread(target = thread_check_progs)
    t.daemon = True
    t.start()
    shell(progs)

main()
atexit.register(save_history)
del os, atexit, readline, rlcompleter, save_history, historyPath
