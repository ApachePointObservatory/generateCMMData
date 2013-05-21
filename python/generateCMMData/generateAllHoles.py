#!/usr/bin/env python
from __future__ import with_statement
"""
Generate data for the UW Brown and Sharp CMM from SDSS "plDrillPos" files.

Choose all reachable holes and order them for efficient measuring.

History
2000-11-18 ROwen    Mod. to reject center hole.
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
2011-10-07 ROwen    Removed run.
                    Renamed runOneFile to generateAllHoles.
                    Modified generateAllHoles to return GenSummary instead of printing messages.
2012-11-14 CCS      Now optimizing measurement order.
2013-05-21 ROwen    Reduced the number of ordering iterations to speed up the program.
                    Minor cleanups to make it work as a command-line script.
                    Moved command-line portion to examples.
"""
import os.path
import re
import numpy
from . import readPlDrillPosData
from . import genSummary
from . import orderPoints

__all__ = ["generateAllHoles"]

DOSTerm = "\r\n"

def generateAllHoles(inFilePath, outDir):
    """Generate one CMM file with all reachable holes from a plPlugMap*.par file.
    
    Return a GenSummary object describing what was done.
    """
#    print "generateAllHoles(inFilePath=%r, outDir=%r)" % (inFilePath, outDir)
    nHolesWritten = 0

    inName = os.path.basename(inFilePath)

    # extract plate number from file name
    try:
        platenum = int(re.split("[-.]", inName)[1])
    except:
        raise RuntimeError, "cannot parse file name: %s" % (inName,)

    dataList, nHolesRead = readPlDrillPosData.readPlDrillPosData(inFilePath)
    nHolesInRange = len(dataList)
    
    # if no data found, complain and quit
    if nHolesInRange <= 0:
        raise RuntimeError("%d holes, but none are reachable" % (nHolesRead,))

    dataArr = numpy.array(list((d["x"], d["y"], d["dia"]) for d in dataList), dtype=float)
        
    # order the points in a way that is efficient to measure
    orderPointsObj = orderPoints.OrderPoints(nIter=50000)
    orderedArr = orderPointsObj(dataArr)        

    # create output file
    outName = "N" + str(platenum) + "A"
    outPath = os.path.join(outDir, outName)
    with file(outPath, "wb") as outFile:
        # write the header
        outFile.write ("#XYZ SC2" + DOSTerm)

        # write the data
        for pt in orderedArr:
            outFile.write ("%11.5f %11.5f  0.0 %8.5f" % (pt[0], pt[1], pt[2]))
            outFile.write (DOSTerm)
            nHolesWritten += 1

    return genSummary.GenSummary(
        fromPath = inFilePath,
        toPath = outPath,
        nHolesRead = nHolesRead,
        nHolesInRange = nHolesInRange,
        nHolesWritten = nHolesWritten,
    )
