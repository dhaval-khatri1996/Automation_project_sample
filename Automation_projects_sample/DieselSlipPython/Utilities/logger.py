from pathlib import Path
import os
import sys
from datetime import date,datetime

def log(status,message):
    print(message)
    print("=======================")
    Path(os.path.expanduser("~\\logs")).mkdir(parents=True, exist_ok=True)
    logMessage = status +"  " + str(datetime.now()) + sys._getframe(1).f_code.co_filename + " - " + sys._getframe(1).f_code.co_name + " : "+ message
    file = getFileHandler()
    file.write(logMessage + "\n")
    file.close

def getFileHandler():
    filename = str(date.today()) + "-execution-log.txt" 
    if os.path.exists(filename):
        fileModifier = 'a' # append if already exists
    else:
        fileModifier = 'w' # make a new file if not
    return open(filename,fileModifier)

