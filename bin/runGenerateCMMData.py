#!/usr/bin/env python
"""Generate CMM data (for the UW Brown and Sharp CMM running Avail) from SDSS "plDrillPos" files.

History
2011-10-07 ROwen    
"""
import sys
import Tkinter
import generateCMMData

filePathList = sys.argv[1:]
# strip first argument if it starts with "-", as happens when run as a Mac application
if filePathList and filePathList[0].startswith("-"):
    filePathList = filePathList[1:]

root = Tkinter.Tk()
root.title("GenerateCMMData")

mainWdg = generateCMMData.GenerateCMMDataWdg(master=root, filePathList=filePathList)
mainWdg.pack(side="left", expand=True, fill="both")
root.mainloop()
