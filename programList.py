import logger

from parse import *

class ProgramList():

	lst = []

	def __init__(self, fd):
		self.lst = read_file(fd)
		self.fd = fd

	def launch(self):
		for prog in self.lst:
			prog.run()

	def start_all(self):
		for p in self.lst:
			try:
				print "start " + p.name
				p.execute()
				logger.log("start prog " + p.name)
			except Exception as e:
				print("Can't start program : ", e)
				logger.log("Can't start program : ", e)

	def kill_all(self):
		for p in self.lst:
			try:
				print "stop " + p.name
				logger.log("stop " + p.name)
				p.kill()
			except Exception as e:
				print("Can't stop program : ", e)
				logger.log("Can't stop program : ", e)

	def check(self):
		for prog in self.lst:
			prog.check()

	def get_status(self):
		for prog in self.lst:
			print(prog.name, " : ", prog.get_status())

	def reload(self):
		for prog in self.lst:
			if hasattr(prog, "keep_old_process"):
				# the program is already running, it needs special care
				prog.reload()
			else:
				if prog.autostart:
					prog.execute()

	def get_by_name(self, prog_name):
		for p in self.lst:
			if (p.name == prog_name):
				return p
		return None