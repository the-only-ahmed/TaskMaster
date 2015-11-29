import sys

def start():
    print "start"

def stop():
    print "stop"

def restart():
    print "restart"

def exit():
    sys.exit()

def status():
    print "status"

def startAll():
    print "startAll"

def stopAll():
    print "stopAll"

def reloadConfig():
    print "reload config File"

def help():
    print "help : get the help menu"
    print "start : start program"
    print "stop : stop program"
    print "restart : restart program"
    print "exit : kill all processes and exit the main program"
    print "status : status of processes"
    print "startAll : start all the processes"
    print "stopAll : stop all the processes"
    print "reload : reload program"
