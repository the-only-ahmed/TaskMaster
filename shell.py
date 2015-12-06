import os

from func import *

cmd = ['status', 'exit', 'stop', 'start', 'restart', 'startAll', 'stopAll', 'reload', 'load', 'help']

cmdNoArg = ['help']
cmd1Arg = ['exit', 'status', 'startAll', 'stopAll', 'reload']
cmd2Arg = ['stop', 'start', 'restart', 'load']

prompt = os.environ['LOGNAME'] + " > "

funcdict = {
                'status' : status,
                'exit' : exitP,
                'stop' : stop,
                'start' : start,
                'restart' : restart,
                'startAll' : startAll,
                'stopAll' : stopAll,
                'reload' : reloadConfig,
                'load' : loadNewConfig,
                'help' : help
            }

historyPath = os.path.expanduser("~/.pyhistory")

def save_history(historyPath=historyPath):
    import readline
    readline.write_history_file(historyPath)

def shell(progs):
    while (True):
        try:
            var = raw_input(prompt).strip().split(' ')
            for v in var:
                v = v.strip()
            if (var[0] in cmdNoArg):
                funcdict[var[0]]()
            elif (var[0] in cmd1Arg):
                funcdict[var[0]](progs)
            elif (var[0] in cmd2Arg):
                if (len(var) != 2):
                    print "wrong argument for " + var[0]
                else:
                    funcdict[var[0]](progs, var[1])
            elif (len(var) > 0 and var[0] != ""):
                print "command not found :", var[0]
        except:
            exitP(progs)
