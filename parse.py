import yaml

from prog import Prog

dict = ['programs', 'cmd', 'numprocs', 'umask', 'workingdir', 'autostart', 'autorestart',
        'exitcodes', 'startretries', 'starttime', 'stopsignal', 'stoptime', 'stdout', 'stderr', 'env']

progs = []

def yamlParser(fd):
    try:
        poop = yaml.load(fd)
        return poop
    except Exception as e:
        print("Can't parse config file because : {0}".format(e))

def read_file(fd):
    try:
        config = yamlParser(fd)
        if not config:
            return False
        for k, v in config.items():
            try:
                prog = Prog(k, v)
                progs.append(prog)
            except Exception as e:
                print("Program error {0}".format(e))
        return progs
    except IOError as e:
            print("Impossible to open config file because : {0}".format(e))
