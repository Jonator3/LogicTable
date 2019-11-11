import LogForm
import sys
from Logger import Log
import traceback


if len(sys.argv) > 1:
	log = Log("log")
	file = open(sys.argv[1], "r")
	lines = file.readlines()
	for line in lines:
		text = line.replace("\n","")
		split = text.split(":")
		if split[0] == "table":
			try:
				pic = LogForm.makePic(split[1])
				LogForm.save(pic, split[2])
				log.print("Saved Table \""+split[1]+"\" as: "+split[2])
			except Exception:
				log.print("Failed to save Table \""+split[1]+"\" as: "+split[2])
		elif split[0] == "settings":
			try:
				if split[1] == "linethickness":
					LogForm.LineThickness = int(split[2])
					log.print("Set LineThickness to: "+split[2])
				elif split[1] == "fontsize":
					LogForm.FontSize = int(split[2])
					log.print("Set FontSize to: "+split[2])
				elif split[1] == "linecolor":
					c = (int(split[2]), int(split[3]), int(split[4]))
					LogForm.LineColor = c
					log.print("Set LineColor to: "+str(c))
				elif split[1] == "bkcolor":
					c = (int(split[2]), int(split[3]), int(split[4]))
					LogForm.BkColor = c
					log.print("Set BkColor to: "+str(c))
				elif split[1] == "fontcolor":
					c = (int(split[2]), int(split[3]), int(split[4]))
					LogForm.FontColor = c
					log.print("Set FontColor to: "+str(c))
				elif split[1] == "headcolor":
					c = (int(split[2]), int(split[3]), int(split[4]))
					LogForm.HeadColor = c
					log.print("Set HeadColor to: "+str(c))
				else:
					raise Exception
			except Exception:
				log.print("\""+text+"\" Failed")
else:
	lastScreen = None
	while True:
		try:
			con = input(">")
			if con == "exit" or con == "stop":
				sys.exit(0)
			elif con.startswith("h"):
				print("")
				print("List of Comands:")
				print("   exit                >>> exit Program")
				print("   stop                >>> exit Program")
				print("")
				print("   BkColor R G B       >>> Set Background Color for Tables")
				print("   HeadColor R G B     >>> Set Head Background Color for Tables")
				print("   FontColor R G B     >>> Set Font Color for Tables")
				print("   LineColor R G B     >>> Set Line Color for Tables")
				print("   FontSize int        >>> Set Font Size for Tables")
				print("   LineThickness int   >>> Set Font Size for Tables")
				print("")
				print("   show formula        >>> Creates ands shows new Table")
				print("   save filename       >>> saves last Table as filename")
				print("")
			elif con.startswith("BkColor "):
				con = con[8:]
				split = con.split(" ")
				c = (int(split[0]), int(split[1]), int(split[2]))
				LogForm.BkColor = c
			elif con.startswith("HeadColor "):
				con = con[10:]
				split = con.split(" ")
				c = (int(split[0]), int(split[1]), int(split[2]))
				LogForm.HeadColor = c
			elif con.startswith("FontColor "):
				con = con[10:]
				split = con.split(" ")
				c = (int(split[0]), int(split[1]), int(split[2]))
				LogForm.FontColor = c
			elif con.startswith("LineColor "):
				con = con[10:]
				split = con.split(" ")
				c = (int(split[0]), int(split[1]), int(split[2]))
				LogForm.LineColor = c
			elif con.startswith("FontSize "):
				con = con[9:]
				LogForm.FontSize = int(con)
			elif con.startswith("LineThikness "):
				con = con[13:]
				LogForm.LineThickness = int(con)
			elif con.startswith("save "):
				con = con[5:]
				print("saving to",con)
				if lastScreen is None:
					print("Can´t save None type!")
				else:
					try:
						LogForm.save(lastScreen, con)
						print("done")
					except Exception:
						print("Can`t save:",con)
			elif con.startswith("show "):
				con = con[5:]
				lastScreen = LogForm.showTable(con)
		except Exception:
			traceback.print_exc()
			print("ignoring Exception")

