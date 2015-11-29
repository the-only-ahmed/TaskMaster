import os
import subprocess

class Prog():
    def __init__(self, name):
        self.name = name
        self.cmd = []
        self.numprocs = 0
        self.umask = 0
        self.workingdir = ""
        self.autostart = True
        self.autorestart = "always"
        self.exitcodes = []
        self.startretries = 0
        self.starttime = 0
        self.stopsignal = ""
        self.stoptime = -1
        self.stdout = subprocess.PIPE
        self.stderr = subprocess.PIPE
        self.env = {}
        self.pid = 0
        self.returnCode = 0


    def setCmd(self, arg):
        tmpList = arg.strip().split(' ')
        for tmp in tmpList:
            tmp = ''.join(e for e in tmp if (e != '\"' and e != '\''))
            self.cmd.append(tmp)

    def setProcs(self, arg):
        self.numprocs = int(arg)

    def setMask(self, arg):
        self.umask = int(arg)

    def setWorkingDir(self, arg):
        self.workingdir = arg.strip()

    def setAutoStart(self, arg):
        self.autostart = arg.strip()

    def setAutoReStart(self, arg):
        self.autorestart = arg.strip()

    def addExitCodes(self, arg):
        self.exitcodes.append(int(arg))

    def setStartRetries(self, arg):
        self.startretries = int(arg)

    def setStartTime(self, arg):
        self.starttime = int(arg)

    def setStopSignal(self, arg):
        self.stopsignal = arg.strip()

    def setStopTime(self, arg):
        self.stoptime = int(arg)

    def setStdOut(self, filename):
        self.stdout = open(filename.strip(), 'w+')

    def setStdErr(self, filename):
        self.stderr = open(filename.strip(), 'w+')

    def addEnv(self, key, value):
        self.env[key.strip()] = value.strip()

    def setPid(self, pid):
        self.pid = pid

    def setReturnCode(self, code):
        self.code = code
