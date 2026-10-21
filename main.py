import shutil
import os
import sys
import time
import readchar
import select
import termios
import tty
import readchar.key as rck


home = os.path.expanduser("~")
truehome = "/home/tlc"
bold = "\033[1m"
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
cwd = os.getcwd()
hl1, hl2 = 0, 0
scroll = 0
scroll2 = 0
scroll3 = True
scroll4 = False

def mainloop(key, # default values
		sidebar = 33,
		sidebarbg = (58, 25, 87),
		bodybg = (90, 41, 135),
		topbg = (75, 35, 110),
		pins = [],
		pinsbold = True,
		pinsleftpad = 3,
		pinsuppad = 9,
		logo = ""
	):

	global hl1, hl2, scroll, scroll2, scroll3, scroll4
	if key == rck.UP:
		hl2 -= 1
		scroll4 = False
		scroll3 = True
	if key == rck.DOWN:
		hl2 += 1
		scroll4 = False
		scroll3 = True

	if key == "w":
		hl1 -= 1
		scroll4 = True
		scroll3 = False
	if key == "s":
		hl1 += 1
		scroll4 = True
		scroll3 = False

	buffer = "" # init stuff
	width, height = shutil.get_terminal_size()
	cwd = os.getcwd()
	contents = os.listdir()
	dirs = []
	files = []
	for i in contents:
		if os.path.isdir(i):
			dirs.append(i)
		else:
			files.append(i)

	dirs.sort()
	files.sort()

	if cwd == "/":
		contents = dirs + files
	else:
		contents = [".."] + dirs + files

	if hl2 >= len(contents):
		hl2 = len(contents) - 1
	elif hl2 < 0:
		hl2 = 0

	if hl1 >= len(pins):
		hl1 = len(pins) - 1
	elif hl1 < 0:
		hl1 = 0

	if scroll3:
		scroll = hl2 - 25
		if scroll < 0:
			scroll = 0

	if scroll4:
		scroll2 = hl1 - 25
		if scroll2 < 0:
			scroll2 = 0

	if key == " " or key == rck.ENTER:
		if scroll3:
			if contents[hl2] in dirs:
				os.chdir(contents[hl2])
				cwd = os.getcwd()
				contents = os.listdir()
				dirs = []
				files = []
				for i in contents:
					if os.path.isdir(i):
						dirs.append(i)
					else:
						files.append(i)

				dirs.sort()
				files.sort()

				if cwd == "/":
					contents = dirs + files
				else:
					contents = [".."] + dirs + files

			elif contents[hl2] == "..":
				os.chdir("/" + "/".join(cwd.split("/")[:-1]))
				cwd = os.getcwd()
				contents = os.listdir()
				dirs = []
				files = []
				for i in contents:
					if os.path.isdir(i):
						dirs.append(i)
					else:
						files.append(i)

				dirs.sort()
				files.sort()

				if cwd == "/":
					contents = dirs + files
				else:
					contents = [".."] + dirs + files

		elif scroll4:
			os.chdir(pins[hl1][1])
			cwd = os.getcwd()
			contents = os.listdir()
			dirs = []
			files = []
			for i in contents:
				if os.path.isdir(i):
					dirs.append(i)
				else:
					files.append(i)

			dirs.sort()
			files.sort()

			if cwd == "/":
				contents = dirs + files
			else:
				contents = [".."] + dirs + files

			hl2 = 0


	bodywidth = width - sidebar
	sidebarbg_ansi = f"\033[48;2;{sidebarbg[0]};{sidebarbg[1]};{sidebarbg[2]}m"
	bodybg_ansi = f"\033[48;2;{bodybg[0]};{bodybg[1]};{bodybg[2]}m"
	topbg_ansi = f"\033[48;2;{topbg[0]};{topbg[1]};{topbg[2]}m"
	logoarr = logo.split("\n")

	for line in range(height):
		buffer += "\033[0m"
		sc1 = line - pinsuppad + scroll2
		if sc1 == hl1 and scroll4:
			buffer += topbg_ansi
		else:
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
		sc = line - 2 + scroll

		if line == 0:
			buffer += topbg_ansi
			buffer += bold + f"{cwd.replace(home, f"{homeico}  Home").replace(truehome, f"{homeico}  Home").replace("/", f"    ")}".center(bodywidth)

		elif sc < len(contents) and sc >= 0:
			if sc == hl2 and scroll3:
				buffer += topbg_ansi
			else:
				buffer += bodybg_ansi
			buffer += bold
			if contents[sc] in dirs:
				buffer += f"     {contents[sc]}".ljust(bodywidth)
			else:
				name = contents[sc]
				if name.endswith(".pdf"):
					fico = "  "
				elif name.endswith(".py"):
					fico = "󰌠  "
				elif name != "..":
					fico = "󰈔  "
				else:
					fico = ""

				buffer += f"   {fico}{name}".ljust(bodywidth)

		else:
			buffer += bodybg_ansi
			buffer += " "*bodywidth

		if line < height - 1:
			buffer += "\r\n"

	sys.stdout.write("\033[2J\033[H" + buffer)
	sys.stdout.flush()


if __name__ == "__main__":
	sys.stdout.write("\033[?25l\033[?1049h")
	sys.stdout.flush()
	key = None
	fd = sys.stdin.fileno()
	oldset = termios.tcgetattr(fd)
	tty.setraw(fd)

	try:
		while True:
			mainloop(key=key, **args)
			key = readchar.readkey()
			if key == rck.CTRL_C:
				break

	except Exception as e:
		print(e)

	sys.stdout.write("\033[?25h\033[?1049l")
	sys.stdout.flush()

	termios.tcsetattr(fd, termios.TCSADRAIN, oldset)


