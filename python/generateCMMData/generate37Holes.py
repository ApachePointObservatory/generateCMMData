#!/usr/bin/env python
from __future__ import with_statement
"""
Generate data for the UW Brown and Sharp CMM from SDSS "plDrillPos" files.

Choose NumHoles holes in a well distributed pattern.

History
2001-10-26 ROwen    First version with history
2001-11-28 ROwen    Increased xMax from 300 to 390, yMax from 200 to 290
                    due to the accurate the new plug plate holding fixture.
                    Also added total number of holes found to status output.
2002-01-04 ROwen    Modified to handle new plDrillPos format.
2003-04-15 ROwen    Modified to use RO.procFiles.
2005-03-01 ROwen    Stopped using xreadlines.
                    Improved error handling.
                    Fixed so it can handle files with small #s of holes.
2005-03-15 ROwen    Stopped importing random (since I wasn't using it).
2010-06-09 ROwen    Expanded xMax, yMax for new CMM (Brown and Sharp 7-10-7)
2010-06-11 ROwen    Modified to use readPlDrillPosData.
                    Modified to use simulated annealling to distribute the holes and order them (instead of
                    sectors). This gives more uniform coverage and perhaps a slight increase in in speed.
2010-06-15 ROwen    Modified to not use RO.procFiles.
2011-10-07 ROwen    Removed run.
                    Renamed runOneFile to generateAllHoles.
                    Modified generateAllHoles to return GenSummary instead of printing messages.
"""
import os.path
import sys
import re
import numpy
from . import readPlDrillPosData
from . import distributePoints
from . import orderPoints
from . import genSummary

__all__ = ["generate37Holes"]

# number of holes to select
NumHoles = 37

# constants
DOSTerm = "\r\n"

def generate37Holes(inFilePath, outDir):
    """Generate one CMM file with 37 well-spaced holes from a plPlugMap*.par file.
    
    Return a GenSummary object describing what was done.
    """
#   print "generate37Holes(inFilePath=%r, outDir=%r)" % (inFilePath, outDir)
    distribPointsObj = distributePoints.DistributePoints(numToSelect = NumHoles)
    orderPointsObj = orderPoints.OrderPoints()

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
    
    if len(dataArr) > NumHoles:
        # Select 37 points that are well distributed across the whole set
        distribArr = distribPointsObj(dataArr)
    else:
        distribArr = dataArr

    # order the points in a way that is efficient to measure
    orderedArr = orderPointsObj(distribArr)
    
    # create output file (in same directory as input file)
    outName = "N" + str(platenum)
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

if __name__ == "__main__":
    debugFiles = ("plDrillPos-0825.par",)
    if True:
        # debug version
        inFilePathList = debugFiles
    else:
        inFilePathList = sys.argv[1:]
    run(inFilePathList, ".")
