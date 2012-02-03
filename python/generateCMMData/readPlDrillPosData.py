"""Read plDrillPos data from stdin

Reject hole outside the range of our Brown and Sharp 7-10-7 CMM

History
2010-06-11 ROwen    Extracted from Generate37Holes.py
2010-06-24 ROwen    Modified to handle modern par files with zDrill (and older files without).
2012-01-03 ROwen    Modified to handle very old par files without xDrill, yDrill.
"""
from __future__ import with_statement
import math
import sys
import re

# debugFiles are processed automatically when run in debug mode
# (run from a .py file instead of a drag-and-drop applet)
debugFiles = ("plDrillPos-0825.par",)

# maximum |x|, |y| for the CMM, in mm
# the CMM full range is 650 x 1000 mm
# and we need a bit of margin to make the measurement (I'm using 10 mm)
xMax, yMax = 490.0, 315.0
holenames = ("OBJECT", "GUIDE", "QUALITY")  # holes to use

# search expression for valid data
dataRegEx = re.compile(r'^drillpos +(?P<name>\w+) +\{.+\}( +[0-9e+-.]+){4} +(?P<x>[0-9e+-.]+) +(?P<y>[0-9e+-.]+)( +[0-9e+-.]+){0,3} +(?P<dia>[0-9e+-.]+)$', re.IGNORECASE)

def readPlDrillPosData(inFilePath):
    """Read data from a plDrillPos file
    
    Inputs:
    - inFilePath: path to file containing hole position data
    
    Return:
    - dataList: sequence of dictionaries with keys: x, y, dia, name; only includes holes that are in bounds
    - nHolesRead: number of holes read (some of which may have been rejected as out of bounds)
    """
    nHolesRead = 0
    gotData = False
    dataList = []

    with file(inFilePath, "rU") as inFile:
        for line in inFile:
            # skip blank lines
            if line == "\n":
                continue
    
            # try to parse data
            # sys.stderr.write ("parsing data :%s:\n" % line) # for debugging
            dataMatched = dataRegEx.search(line)
            # if not data, skip it -- an error if we already saw data
            if not dataMatched:
                if gotData:
                    raise RuntimeError, "bad data mixed in with good; bad data = :%s:" % (line)
            # else figure out if we want to write the data
            else:
                gotData = True
                nHolesRead += 1
                dataDict = dataMatched.groupdict()
                for key in ("x", "y", "dia"):
                    dataDict[key] = float(dataDict[key])
                if dataDict["name"] in holenames and abs(dataDict["x"]) <= xMax and abs(dataDict["y"]) <= yMax:
                    # data is for a hole of interest and that is in range
    
                    radSq = dataDict["x"]**2 + dataDict["y"]**2
                    if radSq < 0.001:
                        continue # skip center hole
    
                    # append data to list
                    dataList.append(dataDict)

    if len(dataList) == 0:
        raise RuntimeError("No valid data found in %r: " % (inFilePath,))
    return dataList, nHolesRead
