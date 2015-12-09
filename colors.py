import logger

class Scolors():
    @classmethod
    def getColor(x, s):
	if type(s) is Scolors:
		return s
	elif s == "pink":
		return Scolors.PINK;
	elif s == "blue":
		return Scolors.BLUE
	elif s == "cyan":
		return Scolors.CYAN
	elif s == "green":
		return Scolors.GREEN
	elif s == "purple":
		return Scolors.PURPLE
	elif s == "red":
		return Scolors.RED
	elif s == "yellow":
		return Scolors.YELLOW
	elif s == "magenta":
		return Scolors.MAGENTA
	elif s == "grey":
		return Scolors.GREY
	elif s == "bold":
		return Scolors.BOLD
	elif s == "underline":
		return Scolors.UNDERLINE
	elif s == "endc":
		return Scolors.ENDC
	else:
		print Scolors.RED + "Wrong Color" + Scolors.ENDC
		logger.log("wrong color")
		return Scolors.ENDC

    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[36m'
    GREEN = '\033[92m'
    PURPLE = '\033[35m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    GREY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'
