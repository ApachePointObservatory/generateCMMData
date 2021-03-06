"""Read plDrillPos data from stdin

Reject hole outside the range of our Brown and Sharp 7-10-7 CMM

History
2010-06-11 ROwen    Extracted from Generate37Holes.py
2010-06-24 ROwen    Modified to handle modern par files with zDrill (and older files without).
2012-01-03 ROwen    Modified to handle very old par files without xDrill, yDrill.
2012-11-14 CCS      Modified to recognize MaNGA holes
2012-11-26 CCS      Modified CMM measurement y range from 315mm to 322.5mm
2014-01-16 CCS      Now recognizes "MANGA_SINGLE" holes.
2015-01-13 CCS      Add flag for using x,y Focal vs Flat positions (anticipation of APOGEE-South)
"""

import sys
import re

# debugFiles are processed automatically when run in debug mode
# (run from a .py file instead of a drag-and-drop applet)
debugFiles = ("plDrillPos-0825.par",)

# maximum |x|, |y| for the CMM, in mm
# the CMM full range is 650 x 1000 mm
# and we need a bit of margin to make the measurement (I'm using 10 mm)
xMax, yMax = 490.0, 322.5
holenames = ("OBJECT", "GUIDE", "QUALITY", "MANGA", "MANGA_SINGLE")  # holes to use

# search expression for valid data
dataRegEx = re.compile(r'^drillpos +(?P<name>\w+) +\{.+\}( +[0-9e+-.]+){2} +(?P<xFocal>[0-9e+-.]+) +(?P<yFocal>[0-9e+-.]+) +(?P<xFlat>[0-9e+-.]+) +(?P<yFlat>[0-9e+-.]+)( +[0-9e+-.]+){0,3} +(?P<dia>[0-9e+-.]+)$', re.IGNORECASE)

def readPlDrillPosData(inFilePath, useFlat=True):
    """Read data from a plDrillPos file

    Inputs:
    - inFilePath: path to file containing hole position data
    - useFlat: if true x,y positions are flat, else focal x,y (as drilled) are used.

    Return:
    - dataList: sequence of dictionaries with keys: x, y, dia, name; only includes holes that are in bounds
    - nHolesRead: number of holes read (some of which may have been rejected as out of bounds)
    """
    nHolesRead = 0
    gotData = False
    if useFlat:
        xType = "xFlat"
        yType = "yFlat"
    else:
        xType = "xFocal"
        yType = "yFocal"
    dataList = []

    with open(inFilePath, "rU") as inFile:
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
                    raise RuntimeError("bad data mixed in with good; bad data = :%s:" % (line))
            # else figure out if we want to write the data
            else:
                gotData = True
                nHolesRead += 1
                dataDict = dataMatched.groupdict()
                for key in (xType, yType, "dia"):
                    dataDict[key] = float(dataDict[key])
                if dataDict["name"] in holenames and abs(dataDict[xType]) <= xMax and abs(dataDict[yType]) <= yMax:
                    # data is for a hole of interest and that is in range

                    radSq = dataDict[xType]**2 + dataDict[yType]**2
                    if radSq < 0.001:
                        continue # skip center hole

                    # append data to list
                    dataList.append(dataDict)
                elif dataDict["name"] in ("GUIDE", "MANGA"):
                    # A manga or guide hole is out of cmm range.
                    print("Essential hole reported out of range, but written anyways", dataDict, file=sys.stderr)
                    dataList.append(dataDict)
                    # raise RuntimeError("Essential hole out of measurement range.")

    if len(dataList) == 0:
        raise RuntimeError("No valid data found in %r: " % (inFilePath,))
    return dataList, nHolesRead
