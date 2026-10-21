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
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
█████  ██████ ██████ ██▙  ▟██
██  ██   ██   ██     ████████
██  ██   ██   ██     ██ ▀▀ ██
█████    ██   ████   ██    ██
██  ██   ██   ██     ██    ██
██  ██   ██   ██     ██    ██
██  ██   ██   ██     ██    ██
Raine's Terminal File Manager
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
"""
}
cwd = os.getcwd()
hl1, hl2 = 0, 0
scroll = 0
scroll2 = 0
scroll3 = True
scroll4 = False

def mainloop(key, # default values
		sidebarbg = (58, 25, 87),
		bodybg = [(90, 41, 135), (100, 49, 145)],
		topbg = (75, 35, 110),
		highlightbg = (115, 63, 161),

		sidebar = 33,
		sizewidth = 70,
		rightreserve = 70,

		pins = [],
		pinsbold = True,
		pinsleftpad = 3,
		pinsuppad = 11,
		logo = "",

		logocol = (161, 255, 107),
		dirfg = (143, 221, 255),
		filefg = (221, 176, 255),
		zipfg = (255, 110, 110),
		mediafg = (161, 255, 242),
		codefg = (181, 255, 187),
		gitfg = (255, 195, 122),

		symlink = (255, 239, 161),
		smallfile = (255, 202, 161),
		largefile = (255, 161, 161)
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

	if key == rck.PAGE_UP:
		hl2 -= 20
		scroll4 = False
		scroll3 = True
	if key == rck.PAGE_DOWN:
		hl2 += 20
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

	def getsizes(contents):
		size = []
		for i in contents:
			if i == "..":
				size.append(["", True, 0])

			elif os.path.islink(i):
				size.append([    f"  {os.path.realpath(i)}", True, 0])

			else:
				s = os.path.getsize(i)
				g = []
				if s >= 1024**8:
					g.append(f"   {s/(1024**8):.2f} YB")
					g.append(2)
				elif s >= 1024**7:
					g.append(f"   {s/(1024**7):.2f} ZB")
					g.append(False)
					g.append(2)
				elif s >= 1024**6:
					g.append(f"   {s/(1024**6):.2f} EB")
					g.append(False)
					g.append(2)
				elif s >= 1024**5:
					g.append(f"   {s/(1024**5):.2f} PB")
					g.append(False)
					g.append(2)
				elif s >= 1024**4:
					g.append(f"   {s/(1024**4):.2f} TB")
					g.append(False)
					g.append(2)
				elif s >= 1024**3:
					g.append(f"   {s/(1024**3):.2f} GB")
					g.append(False)
					g.append(2)
				elif s >= 1024**2:
					g.append(f"   {s/(1024**2):.2f} MB")
					g.append(False)
					g.append(2)
				elif s >= 1024:
					g.append(f"   {s/1024:.2f} KB")
					g.append(False)
					g.append(1)
				else:
					g.append(f"   {s} B")
					g.append(False)
					g.append(1)
				size.append(g)

		return size

	size = getsizes(contents)

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

				size = getsizes(contents)
				hl2 = 0

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
				
				size = getsizes(contents)
				hl2 = 0

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

			size = getsizes(contents)
			hl2 = 0


	bodywidth = width - sidebar
	ansirgb = lambda rgb, mode=48: f"\033[{mode};2;{rgb[0]};{rgb[1]};{rgb[2]}m" 
	sidebarbg_ansi = ansirgb(sidebarbg)
	bodybg_ansi = ansirgb(bodybg[0])
	topbg_ansi = ansirgb(topbg)
	highlightbg_ansi = ansirgb(highlightbg)
	logo_ansi = ansirgb(logocol, 38)

	dir_ansi = ansirgb(dirfg, 38)
	file_ansi = ansirgb(filefg, 38)
	zip_ansi = ansirgb(zipfg, 38)
	media_ansi = ansirgb(mediafg, 38)
	code_ansi = ansirgb(codefg, 38)
	git_ansi = ansirgb(gitfg, 38)

	symlink_ansi = ansirgb(symlink, 38)
	large_ansi = ansirgb(largefile, 38)
	small_ansi = ansirgb(smallfile, 38)
	logoarr = logo.split("\n")

	for line in range(height):
		buffer += "\033[0m"
		sc1 = line - pinsuppad + scroll2
		if sc1 == hl1 and scroll4:
			buffer += topbg_ansi
		else:
			buffer += sidebarbg_ansi

		if (line-pinsuppad) < len(pins) and (line-pinsuppad) >= 0:
			buffer += dir_ansi
			if pinsbold:
				buffer += "\033[1m"

			buffer += str(" "*pinsleftpad + pins[line-pinsuppad][0]).ljust(sidebar)

		elif line < len(logoarr):
			buffer += logo_ansi
			buffer += "\033[1m"
			buffer += logoarr[line].center(sidebar)

		else:
			buffer += " "*sidebar

		buffer += "\033[0m"
		sc = line - 2 + scroll

		if line == 0:
			buffer += topbg_ansi
			buffer += bold + f"{cwd.replace(home, f"{homeico}  Home").replace(truehome, f"{homeico}  Home").replace("/", f"    ")}".center(bodywidth)

		elif sc < len(contents) and sc >= 0:
			bodybg_ansi = ansirgb(bodybg[len(bodybg) - 1 - sc % len(bodybg)])
			if sc == hl2 and scroll3:
				buffer += highlightbg_ansi
			else:
				buffer += bodybg_ansi
			buffer += bold
			if contents[sc] in dirs:
				if os.path.isdir(f"{contents[sc]}/.git"):
					s = f"     {contents[sc]}".ljust(bodywidth - rightreserve)
				else:
					s = f"     {contents[sc]}".ljust(bodywidth - rightreserve)
				if len(s) > bodywidth - rightreserve:
					s = s[:(bodywidth-rightreserve)-3] + "..."
				if os.path.isdir(f"{contents[sc]}/.git") or contents[sc] == ".git":
					buffer += git_ansi + s
				else:
					buffer += dir_ansi + s

				buffer += " "*sizewidth

			else:
				name = contents[sc]
				if name.endswith(".pdf"):
					colour = file_ansi
					fico = "  "
				elif name.endswith(".py"):
					colour = code_ansi
					fico = "󰌠  "

				elif name.endswith(".sh"):
					colour = code_ansi
					fico = "  "
				elif name.startswith(".bash"):
					colour = code_ansi
					fico = "  "
				elif name.endswith(".ps1"):
					colour = code_ansi
					fico = "  "
				elif name.startswith(".vim"):
					colour = code_ansi
					fico = "  "

				elif name.endswith(".log"):
					colour = file_ansi
					fico = "  "

				elif name != "..":
					t = False
					for i in [".mp4", ".mov"]:
						if name.endswith(i):
							colour = media_ansi
							fico = "  "
							t = True

					for i in [".img", ".iso"]:
						if name.endswith(i):
							colour = zip_ansi
							fico = "  "
							t = True

					for i in [".zip", ".gz", ".xz", ".7z", ".zst"]:
						if name.endswith(i):
							colour = zip_ansi
							fico = "  "
							t = True

					for i in [".html", ".htm", ".md", ".sig"]:
						if name.endswith(i):
							colour = media_ansi
							fico = "󰂺  "
							t = True

					for i in [".png", ".jpg", ".avi", ".ico", ".webp", ".jpeg", ".jpng"]:
						if name.endswith(i):
							colour = media_ansi
							fico = "  "
							t = True

					if not t:
						colour = file_ansi
						fico = "󰈔  "
				else:
					colour = dir_ansi
					fico = ""

				s = f"   {fico}{name}".ljust(bodywidth - rightreserve)
				if len(s) > bodywidth - rightreserve:
					s = s[:(bodywidth-rightreserve)-3] + "..."
				buffer += colour + s
				s = f"{size[sc][0]}".ljust(sizewidth)
				if len(s) > sizewidth:
					s = s[:sizewidth-3] + "..."
				if size[sc][2] == 0:
					s = symlink_ansi + s
				elif size[sc][2] == 1:
					s = small_ansi + s
				elif size[sc][2] == 2:
					s = large_ansi + s
				buffer += s

		else:
			bodybg_ansi = ansirgb(bodybg[0])
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
	finally:
		sys.stdout.write("\033[?25h\033[?1049l")
		sys.stdout.flush()

		termios.tcsetattr(fd, termios.TCSADRAIN, oldset)


