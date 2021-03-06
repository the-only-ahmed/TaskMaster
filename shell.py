import os

from colors import Scolors
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

colorSuc = Scolors.GREEN
colorErr = Scolors.RED

color = Scolors.ENDC
endCol = Scolors.ENDC

def save_history(historyPath=historyPath):
    import readline
    readline.write_history_file(historyPath)

def shell(progs, colors):
    if colors is not None:
	global color
	color = Scolors.getColor(colors[0])
    while (True):
        try:
            var = raw_input(color + prompt + endCol).strip().split(' ')
            for v in var:
                v = v.strip()
            if (var[0] in cmdNoArg):
                funcdict[var[0]]()
            elif (var[0] in cmd1Arg):
                if (var[0] != "reload"):
                    funcdict[var[0]](progs)
                else:
                    progs = funcdict[var[0]](progs)
            elif (var[0] in cmd2Arg):
                if (len(var) != 2):
                    print colorErr + "wrong argument for " + var[0] + endCol
                    logger.log("wrong argument for " + var[0])
                else:
                    if (var[0] != "load"):
                        funcdict[var[0]](progs, var[1])
                    else:
                        progs = funcdict[var[0]](progs, var[1])
            elif (len(var) > 0 and var[0] != ""):
                print colorErr + "command not found :" + var[0] + endCol
                logger.log("command not found :" + var[0])
        except Exception as e:
            logger.log("shell Exception : ", e)
            exitP(progs)
