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
from func import *
from prog import Prog
from subprocess import Popen, PIPE

historyPath = os.path.expanduser("~/.pyhistory")

interf = None
progs_lock = None

dict = ['programs', 'cmd', 'numprocs', 'umask', 'workingdir', 'autostart', 'autorestart',
        'exitcodes', 'startretries', 'starttime', 'stopsignal', 'stoptime', 'stdout', 'stderr', 'env']

cmd = ['status', 'exit', 'stop', 'start', 'restart', 'startAll', 'stopAll', 'reload', 'help']

cmdNoArg = ['help']
cmd1Arg = ['exit', 'status', 'startAll', 'stopAll', 'reload']
cmd2Arg = ['stop', 'start', 'restart']

progs = []

processes = []

funcdict = {
                'status' : status,
                'exit' : exitP,
                'stop' : stop,
                'start' : start,
                'restart' : restart,
                'startAll' : startAll,
                'stopAll' : stopAll,
                'reload' : reloadConfig,
                'help' : help
            }

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
        progs_lock.acquire(True)
        progs.check()
        progs_lock.release()
        time.sleep(0.01)

def save_history(historyPath=historyPath):
    import readline
    readline.write_history_file(historyPath)

def shell():
    while (True):
        var = raw_input("$> ").strip().split(' ')
        for v in var:
            v = v.strip()
        if (var[0] in cmdNoArg):
            funcdict[var[0]]()
        elif (var[0] in cmd1Arg):
            funcdict[var[0]](processes)
        elif (var[0] in cmd2Arg):
            if (len(var) != 2):
                print "wrong argument for " + var[0]
            else:
                funcdict[var[0]](processes, var[1])
        elif (var != ""):
            print "command not found :", var

def read_file(fd):
    lines = fd.read().splitlines()
    exit = False;
    env = False;
    for i, line in enumerate(lines):
        if (":" not in line) and (exit == True) :
            key_word = line.strip().split('-')
            progs[-1].addExitCodes(key_word[1].strip())
        else :
            if exit == True:
                exit = False
            key_word = line.strip().split(':')
            if env == True and key_word[0] in dict:
                env = False
            elif env == True and key_word[1] != "" :
                progs[-1].addEnv(key_word[0], key_word[1])
            elif (key_word[0] not in dict) :
                env = False
                newProg = Prog(key_word[0])
                progs.append(newProg)
            else :
                if key_word[0] == 'cmd' :
                    progs[-1].setCmd(key_word[1])
                elif key_word[0] == 'numprocs' :
                    progs[-1].setProcs(key_word[1])
                elif key_word[0] == 'umask' :
                    progs[-1].setMask(key_word[1])
                elif key_word[0] == 'workingdir' :
                    progs[-1].setWorkingDir(key_word[1])
                elif key_word[0] == 'autostart' :
                    progs[-1].setAutoStart(key_word[1])
                elif key_word[0] == 'autorestart' :
                    progs[-1].setAutoReStart(key_word[1])
                elif key_word[0] == 'exitcodes' :
                    if key_word[1] != "" :
                        progs[-1].addExitCodes(key_word[1].strip())
                    else :
                        exit = True
                elif key_word[0] == 'startretries':
                    progs[-1].setStartRetries(key_word[1])
                elif key_word[0] == 'starttime':
                    progs[-1].setStartTime(key_word[1])
                elif key_word[0] == 'stopsignal':
                    progs[-1].setStopSignal(key_word[1])
                elif key_word[0] == 'stoptime':
                    progs[-1].setStopSignal(key_word[1])
                elif key_word[0] == 'stdout':
                    progs[-1].setStdOut(key_word[1])
                elif key_word[0] == 'stderr':
                    progs[-1].setStdErr(key_word[1])
                elif key_word[0] == 'env' :
                    env = True

def main():
    logger.log("BEGIN TASKMASTER")
    signal.signal(signal.SIGINT, signal_handler)
    if os.path.exists(historyPath):
        readline.read_history_file(historyPath)
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        if os.access(sys.argv[1], os.R_OK):
            fd = open(sys.argv[1], 'r')
        else:
            print("File can't be opened")
            logger.log("File can't be opened")
            exit()
    else:
        print("File doesn't exist")
        logger.log("File doesn't exist")
        exit()
    read_file(fd)
    for prg in progs:
        processes.append(prg)
    for proc in processes:
        proc.run()

    progs_lock = threading.Lock()

    # launch a thread to test progs
    t = threading.Thread(target = thread_check_progs)
    t.daemon = True
    t.start()
    shell()

main()
atexit.register(save_history)
del os, atexit, readline, rlcompleter, save_history, historyPath
