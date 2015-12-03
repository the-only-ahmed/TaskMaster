import os
import subprocess

class Prog():
    def __init__(self, name):
        self.name = name
        self.cmd = []
        self.numprocs = 0
        self.umask = 22
        self.workingdir = None
        self.autostart = True
        self.autorestart = "always"
        self.exitcodes = [os.EX_OK]
        self.startretries = 0
        self.starttime = 0
        self.stopsignal = None
        self.stoptime = -1
        self.stdout = subprocess.PIPE
        self.stderr = subprocess.PIPE
        self.env = {}
        self.pid = 0
        self.returnCode = 0
        self.pros = None

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
        self.autostart = bool(arg.strip())

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

    def execute(self):
        self.pros = subprocess.Popen(self.cmd, env=self.env, stdout=self.stdout, stderr=self.stderr, shell=True, cwd=self.workingdir)
        stdoutdata, stderrdata = self.pros.communicate()
        self.setPid(self.pros.pid)
        self.setReturnCode(self.pros.wait())

    def kill(self):
        os.kill(self.pid, 9)

    def run(self):
        if (self.autostart == True):
            self.execute()
