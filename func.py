import sys

def get_by_name(progs, prog_name):
	for p in progs:
		if (p.name == prog_name):
			return p
	return None

def start(progs, prog_name):
	if (progs == None or prog_name == None):
		print "program name or configFile is empty"
		return
	prog = get_by_name(progs, prog_name)
	if (prog == None):
		print prog_name + " is not set"
		return
	try:
		print "start " + prog_name
		prog.execute()
		# logger.log("start prog " + prog_name)
	except Exception as e:
		print("Can't start program : ", e)


def stop(progs, prog_name):
	if progs == None or prog_name == None:
		print "program name or configFile is empty"
		return
	prog = get_by_name(progs, prog_name)
	if (prog == None):
		print prog_name + " is not set"
		return
	try:
		print "stop " + prog_name
		prog.kill()
		# logger.log("stop prog " + prog_name)
	except Exception as e:
		print("Can't stop program : ", e)


def restart(progs, prog_name):
	if progs == None or prog_name == None:
		print "program name or configFile is empty"
		return
	prog = get_by_name(progs, prog_name)
	if (prog == None):
		print prog_name + " is not set"
		return
	try:
		print "restart " + prog_name
		prog.kill()
		prog.execute()
		# logger.log("restart prog " + prog_name)
	except Exception as e:
		print("Can't start program : ", e)

def exitP(progs):
	for p in progs:
		p.kill()
	logger.log("END TASKMASTER")
	print("end of taskmaster")
	sys.exit(os.EX_OK)

def status(processes):
	print "------------------TASKMASTER------------------"
	for proc in processes:
		_name = proc.name
		_returnCode = proc.returnCode
		_pid = proc.pid
		p = proc.pros
		_alive = ' is running'
		if (p is None) or (p is not None and p.poll() is not None):
			_alive = ' is not running'
		print _name + _alive
		# logger.log(_name + _alive);
	print "------------------TASKMASTER------------------"

def startAll(progs):
	for p in progs:
		try:
			print "start " + p.name
			p.execute()
			# logger.log("start prog " + p.name)
		except Exception as e:
			print("Can't start program : ", e)

def stopAll(progs):
	for p in progs:
		try:
			print "stop " + p.name
			p.kill()
			# logger.log("stop prog " + p.name)
		except Exception as e:
			print("Can't stop program : ", e)


def reloadConfig():
	print "reload config File"

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
