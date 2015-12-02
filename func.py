import sys

def start():
    print "start"

def stop():
    print "stop"

def restart():
    print "restart"

def exit():
    sys.exit()

def status(processes):
    print "------------------TASKMASTER------------------"
    for proc in processes:
        _name = proc.prog.name
        _returnCode = proc.prog.returnCode
        _pid = proc.prog.pid
        _alive = ' is running' if proc.p.poll() is None else ' is not running'
        print _name + _alive
    print "------------------TASKMASTER------------------"

def startAll():
    print "startAll"

def stopAll():
    print "stopAll"

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
