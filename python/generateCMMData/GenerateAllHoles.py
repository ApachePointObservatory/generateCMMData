#!/usr/bin/env python
from __future__ import with_statement
"""
Generates data for the UW Brown and Sharp CMM from SDSS "plDrillPos" files.

The holes are output in the same order in which they are read, since they are already
in an order that makes for efficient drilling.

History
mod. to reject center hole. R.O. 11/16/00
2001-10-26 ROwen    Mod. to use procFiles 2, xreadlines and random instead of whrandom.
2001-11-28 ROwen    Oncreased xMax from 300 to 390, yMax from 200 to 290
                    due to the accurate the new plug plate holding fixture.
                    Also added total number of holes found to status output.
2002-01-04 ROwen    Modified to handle new plDrillPos format.
2003-04-15 ROwen    Modified to use RO.procFiles.
2005-03-01 ROwen    Stopped using xreadlines.
                    Improved error handling.
2005-03-09 ROwen    Fixed corruption that crept in.
2005-03-15 ROwen    Stopped importing random (since I wasn't using it).
2010-06-09 ROwen    Expanded xMax, yMax for new CMM (Brown and Sharp 7-10-7).
                    Removed unused parameter maxHoles.
2010-06-11 ROwen    Modified to use readPlDrillPosData.
2010-06-15 ROwen    Modified to not use RO.procFiles.
"""
import os.path
import sys
import re
import readPlDrillPosData

Debug = False

# debugFiles are processed automatically when run in debug mode
debugFiles = ("plDrillPos-0825.par",)

DOSTerm = "\r\n"

def run(inFilePathList, outDir):
    if not inFilePathList:
        print "No files specified; nothing done"
        return
    for inFilePath in inFilePathList:
        runOneFile(inFilePath, outDir)

def runOneFile(inFilePath, outDir):
#    print "run(inFilePath=%r, outDir=%r)" % (inFilePath, outDir)
    nHolesWritten = 0

    inName = os.path.basename(inFilePath)

    # extract plate number from file name
    try:
        platenum = int(re.split("[-.]", inName)[1])
    except:
        raise RuntimeError, "cannot parse file name: %s" % (inName)

    dataList, nHolesRead = readPlDrillPosData.readPlDrillPosData(inFilePath)
    nHolesInRange = len(dataList)
    
    # if no data found, complain and quit
    if nHolesInRange <= 0:
        raise RuntimeError("%d holes, but none are reachable" % (nHolesRead,))

    # report # of holes found
    print "%d holes found, %d are reachable" % (nHolesRead, nHolesInRange,)

    # create output file
    outName = "N" + str(platenum) + "A"
    outDir = os.path.join(outDir, outName)
    print "creating output file:", outName
    with open(outDir, "wb") as outFile:
        # write the header
        outFile.write ("#XYZ SC2" + DOSTerm)
        
        # write holes
        for outDict in dataList:
            outFile.write ("%(x)11.5f %(y)11.5f  0.0 %(dia)8.5f" % (outDict))
            outFile.write (DOSTerm)
            nHolesWritten += 1
    print "wrote file:", outName, "with", nHolesWritten, "holes"


if __name__ == "__main__":
    if Debug:
        # debug version
        inFilePathList = debugFiles
    else:
        inFilePathList = sys.argv[1:]
    run(inFilePathList, ".")