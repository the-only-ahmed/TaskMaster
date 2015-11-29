import os
import sys
import time
import subprocess
from threading import Thread
from prog import Prog

class Execution(Thread):

    def __init__(self, prog):
        Thread.__init__(self)
        self.prog = prog

    def run(self):
        start = time.ctime()
        proc = subprocess.Popen(self.prog.cmd, env=self.prog.env, stdout=self.prog.stdout, stderr=self.prog.stderr)
        self.prog.setPid(proc.pid)
        self.prog.setReturnCode(proc.wait())
        # if (self.prog.stoptime > -1):
        # os.killpg(proc.pid, signal.SIGTERM)
            # time.sleep(self.prog.stoptime)
            # if p.is_alive():
            # self.terminate()

        # i = 0
        # while i < 20:
        #     sys.stdout.write(self.lettre)
        #     sys.stdout.flush()
        #     attente = 0.2
        #     attente += random.randint(1, 60) / 100
        #     time.sleep(attente)
        #     i += 1
