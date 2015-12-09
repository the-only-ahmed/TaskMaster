import os
import sys
import logger

from colors import Scolors
from programList import ProgramList
from processStatusEnum import ProcessStatusEnum

colorSuc = Scolors.GREEN
colorErr = Scolors.RED
colorEnd = Scolors.ENDC

def start(progs, prog_name):
	if (progs == None or prog_name == None):
		print colorErr + "program name or configFile is empty" + colorEnd
		logger.log("program name or configFile is empty")
		return

	prog = progs.get_by_name(prog_name)
	if (prog == None):
		print prog_name + " is not set"
		logger.log(prog_name + " is not set")
		return

	try:
		print "start " + prog_name
		prog.execute()
		logger.log("start prog " + prog_name)
	except Exception as e:
		print("Can't start program : ", e)
		logger.log("Can't start program : ", e)


def stop(progs, prog_name):
	if progs == None or prog_name == None:
		print colorErr + "program name or configFile is empty" + colorEnd
		logger.log("program name or configFile is empty")
		return

	prog = progs.get_by_name(prog_name)
	if (prog == None):
		print prog_name + " is not set"
		logger.log(prog_name + " is not set")
		return

	try:
		if prog.nb_proc_status(ProcessStatusEnum.RUNNING) == 0:
			print("This program is not running.")
			logger.log("This program is not running.")
			return
		print "stop " + prog_name
		prog.kill()
		logger.log("stop prog " + prog_name)
	except Exception as e:
		print("Can't stop program : ", e)
		logger.log("Can't stop program : ", e)


def restart(progs, prog_name):
	if progs == None or prog_name == None:
		print colorSuc + "program name or configFile is empty" + colorEnd
		logger.log("program name or configFile is empty")
		return
	prog = progs.get_by_name(prog_name)
	if (prog == None):
		print prog_name + " is not set"
		logger.log(prog_name + " is not set")
		return
	try:
		print "restart " + prog_name
		logger.log("restart prog " + prog_name)
		stop(progs, prog_name)
		# prog.kill()
		# prog.execute()
		start(progs, prog_name)
	except Exception as e:
		print("Can't restart program : ", e)
		logger.log("Can't restart program : ", e)

def exitP(progs):
	if progs is not None:
		progs.kill_all()
	logger.log("END TaskMaster")
	print(Scolors.YELLOW + "end of TaskMaster" + colorEnd)
	sys.exit(os.EX_OK)

def status(programs):
	print Scolors.CYAN + "------------------TASKMASTER------------------" + colorEnd
	logger.log("------------------TASKMASTER------------------")
	if programs is not None:
		programs.get_status()
	else:
		logger.log("no config file loaded")
		print "NO CONFIG FILE LOADED"
	logger.log("------------------TASKMASTER------------------")
	print Scolors.CYAN + "------------------TASKMASTER------------------" + colorEnd

def startAll(progs):
	if progs is not None:
		progs.start_all()
	else:
		logger.log("no config file loaded")
		print "NO CONFIG FILE LOADED"

def stopAll(progs):
	if progs is not None:
		progs.kill_all()
	else:
		logger.log("no config file loaded")
		print "NO CONFIG FILE LOADED"

def reloadConfig(old_progs):
	if old_progs is None:
		logger.log("no config file loaded")
		print "NO CONFIG FILE LOADED"
		return None

	logger.log("TaskMaster reloaded")
	print "TaskMaster reloaded"
	new_progs = ProgramList(old_progs.fd)
	for oprog in old_progs.lst:
		for nprog in new_progs.lst:
			# only program which we care about processes should be keep
			if oprog.name == nprog.name:
				oprog.keep_running_process(nprog)
				break

	# now all the progs are in new_progs
	new_progs.reload()
	return new_progs

def loadNewConfig(progs, file_name):
	logger.log("loading file")
	print "loading file"
	if os.access(file_name, os.R_OK):
		fd = open(file_name, 'r')
	else:
		print("File can't be opened")
		logger.log("File can't be opened")
		return
	if progs is not None:
		progs.kill_all()
	progs = ProgramList(fd)
	progs.launch()
	return progs

def help():
	print "help : get the help menu"
	print "start : start program"
	print "stop : Stop the main program"
	print "restart : restart program"
	print "exit : kill all processes and exit the main program"
	print "status : See the status of all the programs described in the config file"
	print "startAll : start all the processes"
	print "stopAll : stop all the processes"
	print "reload : Reload the configuration file without stopping the main program"
	print "load : Load new configuration file without stopping the main program"
