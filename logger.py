import datetime

LOG_PATH = "./log.txt"

def log(s, *exp):
	f = open(LOG_PATH, "a")
	f.write("[" + str(datetime.datetime.now()) + "] " + s + str(exp) + "\n")
	f.close()