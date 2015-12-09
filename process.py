import os
import logger
import subprocess
import datetime
import signal

from processStatusEnum import ProcessStatusEnum
from autoRestartEnum import AutoRestartEnum

class Process():

	popen = None
	kill_by_user = False

	def __init__(self, name, cmd):
		self.name = name
		self.cmd = cmd

	def set_execution_vars(self, stdout, stderr, nenv, workingdir, umask):
		self.stdout = stdout
		self.stderr = stderr
		self.env = nenv
		self.workingdir = workingdir
		self.umask = umask
		self.nb_start_retries = 0

	def execute(self):
		"""Require that set_execution_vars has already been called"""
		self.nb_start_retries += 1
		kill_by_user = False
		try:
			stdoutf = self.open_standard_files(self.stdout)
			stderrf = self.open_standard_files(self.stderr)
			self.cmd = self.umask + self.cmd
			self.popen = subprocess.Popen(self.cmd,
					stdout = stdoutf, stderr = stderrf,
					env = self.env, shell = True, cwd = self.workingdir)
			self.starttime = datetime.datetime.now()
			self.closetime = None
		except Exception as e:
			print("Can't launch process {0} because {1}.".
					format(self.name, e))
			logger.log("Can't launch process {0} because {1}.".
					format(self.name, e))

	def check(self, autorestart, exitcodes, startretries, starttime, stoptime):
		"""Require that set_execution_vars has already been called"""
		if not self.popen:
			return False
		rv = self.popen.poll()
		# test if force kill needed
		self.force_kill_if_needed(stoptime)
		# if program returned
		if rv != None:
			# test if process recently quitted
			if not hasattr(self, "closetime") or not self.closetime:
				self.closetime = datetime.datetime.now()
				logger.log("process in prog " + self.name + \
						" has stop, return code : " + str(rv))

			# restart if needed
			self.restart_if_needed(autorestart, exitcodes, startretries, starttime, rv)

	def restart_if_needed(self, autorestart, exitcodes, startretries, starttime, rv):
		"""Test if need restart"""
		# test if var allow restart
		if self.nb_start_retries > startretries or self.kill_by_user:
			return False
		if autorestart == AutoRestartEnum.never or \
				startretries < 1:
			return
		# print("##", self.name, " return_code_is_allowed ", self.return_code_is_allowed(rv, exitcodes))
		# print("##", self.name, " lived_enough ", not self.lived_enough(starttime))
		if autorestart == AutoRestartEnum.unexpected and \
				self.return_code_is_allowed(rv, exitcodes) and \
				self.lived_enough(starttime):
			return False
		# print("execute")
		self.execute()

	def return_code_is_allowed(self, rc, exitcodes):
		# if exitcodes is only one code
		# print(exitcodes, " ==? ", rc, " => ", rc == exitcodes)
		print ("exit code ", rc)
		if not type(exitcodes) is list:
			return rc == exitcodes
		# if exitcodes is a list of exitcode
		for ec in exitcodes:
			if ec == rc:
				return True
		return False

	def lived_enough(self, starttime):
		"""Return true if the progs lifetime was too short."""
		# The program wasn't started/killed at all
		if not hasattr(self, "starttime") or not hasattr(self, "closetime") \
 				or not starttime:
			return True
		# Test program lifetime
		td = datetime.timedelta(seconds = starttime)
		if (self.closetime - self.starttime) <= td:
			return False
		return True

	def get_status(self, exitcodes):
		if not self.popen:
			return ProcessStatusEnum.NOT_LAUNCH
		if self.popen.poll() == None:
			return ProcessStatusEnum.RUNNING
		streamdata = self.popen.communicate()[0]
		rc = self.popen.returncode
		if self.return_code_is_allowed(rc, exitcodes):
			return ProcessStatusEnum.STOP_OK
		else:
			return ProcessStatusEnum.STOP_KO

	def check_pid_is_alive(self, pid):
		try:
			os.kill(pid, 0)
		except OSError:
			return False
		else:
			return True

	def open_standard_files(self, file_name):
		if file_name == None:
			return
		try:
			fd = open(file_name, "a+")
			return fd
		except Exception as e:
			print("Stantard file for {0} can't be open because {1}.".
					format(self.name, e))
			logger.log("Stantard file for {0} can't be open because {1}.".
					format(self.name, e))
			return None

	def kill(self, stopsignal):
		kill_by_user = True
		if self.popen and not self.popen.poll():
			if self.check_pid_is_alive(self.popen.pid):
				# print("kill ", Process.print_signal(stopsignal), stopsignal, " pid ", self.popen.pid)
				os.kill(self.popen.pid, stopsignal)
				logger.log("process in prog " + self.name + " has been killed")
				self.closetime = datetime.datetime.now()

	def force_kill_if_needed(self, stoptime):
		if not hasattr(self, "closetime") or self.closetime == None:
			return
		if not self.check_pid_is_alive(self.popen.pid) or \
				not hasattr(self, "closetime") or self.closetime == None or \
				stoptime == None:
			return
		diff = (datetime.datetime.now() - self.closetime)
		if diff > datetime.timedelta(seconds = stoptime):
			logger.log("force kill of process for prog " + self.name)
			os.kill(self.popen.pid, 9)
