import os
import sys
import time
import subprocess
from prog import Prog

class Process():

    def __init__(self, prog):
        self.prog = prog
        self.p = 0
        # thread = threading.Thread(target=self.run, args=())

    def run(self):
        start = time.ctime()
        self.p = subprocess.Popen(self.prog.cmd, env=self.prog.env, stdout=self.prog.stdout, stderr=self.prog.stderr, shell=True, cwd=self.prog.workingdir)

        stdoutdata, stderrdata = self.p.communicate()
        self.prog.setPid(self.p.pid)
        self.prog.setReturnCode(self.p.wait())
