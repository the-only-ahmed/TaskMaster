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
import argparse

from daemon import *
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
            if progs is not None:
		progs.check()
            progs_lock.release()
            time.sleep(0.01)
        except:
            exit()

def check_fileExistance(path):
    if os.path.isfile(path):
        if os.access(path, os.R_OK):
            fd = open(path, 'r')
            return fd
        else:
            print("File can't be opened")
            logger.log("File can't be opened")
            return
    else:
        print("File doesn't exist")
        logger.log("File doesn't exist")
        return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--colors", help="add colors to shell", nargs=1)
    parser.add_argument("-d", "--daemon", help="run program as daemon", action="store_true")
    parser.add_argument("-f", "--file", help="add configuration file", nargs=1)
    parser.add_argument("--stop", help="stop the program", action="store_true")
    # parser.add_argument("--start", help="start", action="store_true")
    # parser.add_argument("--restart", help="restart", action="store_true")
    args = parser.parse_args()
    fd = None
    if args.stop:
        taskMasterStop()
    if conf["args"].daemon:
        daemonize()
    if (args.file != None):
        fd = check_fileExistance(args.file[0])
    if (fd is not None):
        global progs
        progs = ProgramList(fd)
        progs.launch()

    print "BEGIN TASKMASTER"
    logger.log("BEGIN TASKMASTER")
    signal.signal(signal.SIGINT, signal_handler)

    if os.path.exists(historyPath):
        readline.read_history_file(historyPath)

    global progs_lock
    progs_lock = threading.Lock()

    # launch a thread to test progs
    t = threading.Thread(target = thread_check_progs)
    t.daemon = True
    t.start()
    shell(progs, args.colors)

main()
atexit.register(save_history)
del os, atexit, readline, rlcompleter, save_history, historyPath
