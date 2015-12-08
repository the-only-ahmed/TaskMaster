import os
import signal
import subprocess
import logger

from process import Process
from autoRestartEnum import AutoRestartEnum
from processStatusEnum import ProcessStatusEnum

class NoCmdException(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Program " + self.name + " doesn't have command to execute"

class UnknowSignalError(Exception):
    def __init__(self, _name):
        self.name = _name

    def __str__(self):
        return 'unknow signal ' + self.name

class Prog():
    """
    Init Program
    """

    numprocs = 1
    cmd = False
    umask = 22
    workingdir = None
    autostart = True
    autorestart = AutoRestartEnum.unexpected
    exitcodes = os.EX_OK # a revoir
    startretries = 0
    starttime = None
    stopsignal = signal.SIGTERM
    stoptime = None
    stdout = None
    stderr = None
    env = {}
    pid = 0
    returnCode = 0
    pros = None
    processes = []

    def __init__(self, name, dic):
        self.name = name
        for k, v in dic.items():
            setattr(self, k, v)
        if not self.cmd:
            raise NoCmdException(name)
            return
        self.autorestart = AutoRestartEnum.fromstr(self.autorestart)
        if type(self.stopsignal) == str:
            self.stopsignal = Prog.signal_from_str(self.stopsignal)
        for i in range(0, self.numprocs):
            self.processes.append(Process(self.name, self.cmd))

    """
    Set Program Attributes
    """

    @classmethod
    def signal_from_str(x, s):
        s = s.upper()
        if s == "TERM":
            return signal.SIGTERM
        if s == "HUP":
            return signal.SIGHUP
        if s == "INT":
            return signal.SIGINT
        if s == "QUIT":
            return signal.SIGQUIT
        if s == "KILL":
            return signal.SIGKILL
        if s == "USR1":
            return signal.SIGUSR1
        if s == "USR2":
            return signal.SIGUSR2
        raise UnknowSignalError(s)

    def setCmd(self, arg):
        # tmpList = arg.strip().split(' ')
        # for tmp in tmpList:
        #     tmp = ''.join(e for e in tmp if (e != '\"' and e != '\''))
        #     self.cmd.append(tmp)
        self.cmd = arg.strip()

    def setProcs(self, arg):
        self.numprocs = int(arg.strip())

    def setMask(self, arg):
        self.umask = int(arg.strip())

    def setWorkingDir(self, arg):
        self.workingdir = arg.strip()

    def setAutoStart(self, arg):
        self.autostart = bool(arg.strip())

    def setAutoReStart(self, arg):
        self.autorestart = AutoRestartEnum.fromstr(arg.strip())

    def addExitCodes(self, arg):
        self.exitcodes.append(int(arg.strip()))

    def setStartRetries(self, arg):
        self.startretries = int(arg.strip())

    def setStartTime(self, arg):
        self.starttime = int(arg.strip())

    def setStopSignal(self, arg):
        if type(arg) == str:
            self.stopsignal = Prog.signal_from_str(arg.strip())
        else:
            self.stopsignal = arg

    def setStopTime(self, arg):
        self.stoptime = int(arg)

    def setStdOut(self, filename):
        self.stdout = filename.strip()

    def setStdErr(self, filename):
        self.stderr = filename.strip()

    def addEnv(self, key, value):
        self.env[key.strip()] = value.strip()

    def setPid(self, pid):
        self.pid = pid

    def setReturnCode(self, code):
        self.code = code

    """
    Program Methodes
    """

    def get_expanded_env(self):
        new_env = os.environ
        if not hasattr(self, "env"):
            return new_env
        for k, v in self.env.items():
            new_env[k] = str(v)
        return new_env

    def relaunch(self):
        self.execute()

    def check_pros(self):
        if (len(self.processes) < self.numprocs):
            for i in range(len(self.processes), self.numprocs):
                self.processes.append(Process(self.name, self.cmd))

    def execute(self):
        self.check_pros()
        logger.log("execute " + self.name)
        new_env = self.get_expanded_env()
        for proc in self.processes:
            proc.set_execution_vars(self.stdout, self.stderr, new_env, \
                    self.workingdir, "umask {:03d};".format(self.umask))
            proc.execute()
        # self.pros = subprocess.Popen(self.cmd, env=self.env, stdout=self.stdout, stderr=self.stderr, shell=True, cwd=self.workingdir)
        # stdoutdata, stderrdata = self.pros.communicate()
        # self.setPid(self.pros.pid)
        # self.setReturnCode(self.pros.wait())

    def check(self):
        for proc in self.processes:
            proc.check(self.autorestart, self.exitcodes, self.startretries, \
                    self.starttime, self.stoptime)

    def kill(self):
        for proc in self.processes:
            proc.kill(self.stopsignal)
        # os.kill(self.pid, 9)

    def run(self):
        if (self.autostart == True):
            self.execute()


    def nb_proc_status(self, status):
        fil = filter(lambda x :
                x.get_status(self.exitcodes) == status, self.processes)
        return len(list(fil))

    def get_status(self):
        if not self.processes or len(self.processes) == 0:
            return "no process"
        nb_proc_not_launched = self.nb_proc_status(ProcessStatusEnum.NOT_LAUNCH)
        nb_proc_running = self.nb_proc_status(ProcessStatusEnum.RUNNING)
        nb_proc_ok = self.nb_proc_status(ProcessStatusEnum.STOP_OK)
        nb_proc_ko = self.nb_proc_status(ProcessStatusEnum.STOP_KO)
        return "{0} process running, {1} ok, {2} ko and {3} not launched". \
                format(nb_proc_running, nb_proc_ok, nb_proc_ko, nb_proc_not_launched)


    def reload(self):
        """To use only if the program is running and is being reloaded"""
        newps = []
        if len(self.processes) < self.numprocs:
            for x in range(0, (self.numprocs - len(self.processes))):
                newp = Process(self.name, self.cmd)
                self.processes.append(newp)
                newps.append(newp)
        if self.autostart:
            for prog in newps:
                prog.execute()

    def is_running(self):
        return self.nb_proc_status(ProcessStatusEnum.RUNNING) > 0

    def keep_running_process(self, nprog):
        """
        Return true if the program's processes should be keep
        while reloading this program.
        """
        if nprog.name != self.name or not self.is_running():
            return False
        erase_old_process = self.reload_has_substantive_change(nprog)
        if erase_old_process:
            self.kill()
        else:
            nprog.processes = self.processes
            nprog.keep_old_process = True
        return erase_old_process


    """
    Class toString Methode
    """
    def __str__(self):
        return "Program<" + self.name + ">"
