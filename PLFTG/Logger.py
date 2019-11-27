import os
import datetime

class Log(object):

    def __init__(self, name="log"):
        self.fileName = name+".txt"
        self.file = open(self.fileName, "w", encoding="utf-8")
        self.print("New LogFile created\n")

    def print(self, content):
        time = datetime.datetime.now()
        text = time.strftime("[%H:%M:%S] ") + content
        text = text.replace("\n", "\n          ")+ "\n"
        self.file.write(text)

    def close(self):
        self.file.close()
