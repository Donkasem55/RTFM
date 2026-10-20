import shutil
import os
import sys
import time
import readchar

homeico = ""
fldico = ""
args = {
	"pins": [
		(f"{homeico}  Home", os.path.expanduser("~")),
		(f"{fldico}  Downloads", os.path.expanduser("~/Downloads")),
		(f"{fldico}  Documents", os.path.expanduser("~/Documents")),
		(f"{fldico}  Pictures", os.path.expanduser("~/Pictures")),
		(f"{fldico}  /", "/")
	],
	"logo": """
█████  ██████ ██████ ███  ███
██  ██   ██   ██     ████████
██  ██   ██   ██     ██ ██ ██
█████    ██   ████   ██    ██
██  ██   ██   ██     ██    ██
██  ██   ██   ██     ██    ██
██  ██   ██   ██     ██    ██
"""
}

def mainloop(key, # default values
		sidebar = 33,
		sidebarbg = (58, 25, 87),
		bodybg = (75, 35, 110),
		pins = [],
		pinsbold = True,
		pinsleftpad = 3,
		pinsuppad = 9,
		logo = ""
	):

	buffer = "" # init stuff
	width, height = shutil.get_terminal_size()

	bodywidth = width - sidebar
	sidebarbg_ansi = f"\033[48;2;{sidebarbg[0]};{sidebarbg[1]};{sidebarbg[2]}m"
	bodybg_ansi = f"\033[48;2;{bodybg[0]};{bodybg[1]};{bodybg[2]}m"
	logoarr = logo.split("\n")

	for line in range(height):
		buffer += sidebarbg_ansi

		if (line-pinsuppad) < len(pins) and (line-pinsuppad) >= 0:
			if pinsbold:
				buffer += "\033[1m"

			buffer += str(" "*pinsleftpad + pins[line-pinsuppad][0]).ljust(sidebar)

		elif line < len(logoarr):
			buffer += logoarr[line].center(sidebar)

		else:
			buffer += " "*sidebar

		buffer += "\033[0m"

		buffer += bodybg_ansi
		buffer += " "*bodywidth
		if line < height - 1:
			buffer += "\n"

	sys.stdout.write("\033[2J\033[H" + buffer)
	sys.stdout.flush()


if __name__ == "__main__":
	sys.stdout.write("\033[?25l\033[?1049h")
	sys.stdout.flush()
	key = None
	try:
		while True:
			mainloop(key=key, **args)
			key = readchar.readkey()
	except:
		pass

	sys.stdout.write("\033[?25h\033[?1049l")
	sys.stdout.flush()


