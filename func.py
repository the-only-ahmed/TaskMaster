import os
import sys
import logger

from programList import ProgramList
from processStatusEnum import ProcessStatusEnum

def start(progs, prog_name):
	if (progs == None or prog_name == None):
		print "program name or configFile is empty"
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
		print "program name or configFile is empty"
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
		print "program name or configFile is empty"
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
	progs.kill_all()
	logger.log("END TaskMaster")
	print("end of TaskMaster")
	sys.exit(os.EX_OK)

def status(programs):
	print "------------------TASKMASTER------------------"
	logger.log("------------------TASKMASTER------------------")
	programs.get_status()
	logger.log("------------------TASKMASTER------------------")
	print "------------------TASKMASTER------------------"

def startAll(progs):
	progs.start_all()

def stopAll(progs):
	progs.kill_all()

def reloadConfig(old_progs):
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