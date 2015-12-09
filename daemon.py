PID_FILE = "/tmp/taskmaster.pid"

def startDaemon():
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)

        # decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)

    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    si = file(DEV_NULL, 'r')
    so = file(DEV_NULL, 'a+')
    se = file(DEV_NULL, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

    # write pidfile
    atexit.register(delPid)
    pid = str(os.getpid())
    file(PID_FILE,'w+').write("%s\n" % pid)

def getTaskPid():
    try:
        pidFile = file(PID_FILE, 'r')
        pid = int(pidFile.read().strip())
        pidFile.close()
    except IOError:
        pid = None
    return pid

def daemonize():
    pid = getTaskPid()
    if pid:
        message = Scolors.RED + "pidfile %s already exist. Tasmaster already running ?\n" + Scolors.ENDC
        sys.stderr.write(message % PID_FILE)
        sys.exit(1)
    startDaemon()

def taskMasterStop():
    """Stop the TaskMaster"""
    pid = getTaskPid()
    if not pid:
        message = Scolors.RED + "pidfile %s does not exist, Taskmaster not running in daemon?\n" + Scolors.ENDC
        sys.stderr.write(message % PID_FILE)
        return
    try:
        while 42:
            os.kill(pid, SIGTERM)
            time.sleep(0.1)
    except OSError, err:
        err = str(err)
        if err.find("No such process") > 0:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
            else:
                print str(err)
                sys.exit(1)
