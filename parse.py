from prog import Prog

dict = ['programs', 'cmd', 'numprocs', 'umask', 'workingdir', 'autostart', 'autorestart',
        'exitcodes', 'startretries', 'starttime', 'stopsignal', 'stoptime', 'stdout', 'stderr', 'env']

progs = []

def read_file(fd):
    lines = fd.read().splitlines()
    exit = False;
    env = False;
    for i, line in enumerate(lines):
        if (":" not in line) and (exit == True) :
            key_word = line.strip().split('-')
            progs[-1].addExitCodes(key_word[1].strip())
        else :
            if exit == True:
                exit = False
            key_word = line.strip().split(':')
            if env == True and key_word[0] in dict:
                env = False
            elif env == True and key_word[1] != "" :
                progs[-1].addEnv(key_word[0], key_word[1])
            elif (key_word[0] not in dict) :
                env = False
                newProg = Prog(key_word[0])
                progs.append(newProg)
            else :
                if key_word[0] == 'cmd' :
                    progs[-1].setCmd(key_word[1])
                elif key_word[0] == 'numprocs' :
                    progs[-1].setProcs(key_word[1])
                elif key_word[0] == 'umask' :
                    progs[-1].setMask(key_word[1])
                elif key_word[0] == 'workingdir' :
                    progs[-1].setWorkingDir(key_word[1])
                elif key_word[0] == 'autostart' :
                    progs[-1].setAutoStart(key_word[1])
                elif key_word[0] == 'autorestart' :
                    progs[-1].setAutoReStart(key_word[1])
                elif key_word[0] == 'exitcodes' :
                    if key_word[1] != "" :
                        progs[-1].addExitCodes(key_word[1].strip())
                    else :
                        exit = True
                elif key_word[0] == 'startretries':
                    progs[-1].setStartRetries(key_word[1])
                elif key_word[0] == 'starttime':
                    progs[-1].setStartTime(key_word[1])
                elif key_word[0] == 'stopsignal':
                    progs[-1].setStopSignal(key_word[1])
                elif key_word[0] == 'stoptime':
                    progs[-1].setStopTime(key_word[1])
                elif key_word[0] == 'stdout':
                    progs[-1].setStdOut(key_word[1])
                elif key_word[0] == 'stderr':
                    progs[-1].setStdErr(key_word[1])
                elif key_word[0] == 'env' :
                    env = True
    return progs