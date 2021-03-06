#!/usr/bin/env python
"""
Generate data for the UW Brown and Sharp CMM from SDSS "plDrillPos" files.

Choose NumHoles holes in a well distributed pattern and order them for efficient measuring.

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
2013-05-21 ROwen    Reduced the number of ordering iterations to speed up the program.
                    Moved command-line portion to examples.
2014-01-02 CS       Forced all Manga and Guide holes to be measured. If other holes remain,
                    37 are randomly measured
2014-01-13 CS       Adjust to allow use of focal vs flat positions
2020-09-10 JSG      Add new version with 50% of single BOSS + APOGEE (400 holes) for SDSS-V.
"""

import os.path
import re
import numpy
from . import readPlDrillPosData
from . import genSummary
from . import orderPoints
from . import distributePoints

__all__ = ["generate400Holes"]

# number of holes to select
NumHoles = 400

# constants
DOSTerm = "\r\n"

def generate400Holes(inFilePath, outDir, useFlat=True):
    """Generate one CMM file with 400 well-spaced holes from a plPlugMap*.par file.

    Return a GenSummary object describing what was done.
    """
#   print "generate37Holes(inFilePath=%r, outDir=%r)" % (inFilePath, outDir)
    if useFlat:
        xType = "xFlat"
        yType = "yFlat"
    else:
        xType = "xFocal"
        yType = "yFocal"
    nHolesWritten = 0

    inName = os.path.basename(inFilePath)

    # extract plate number from file name
    try:
        platenum = int(re.split("[-.]", inName)[1])
    except:
        raise RuntimeError("cannot parse file name: %s" % (inName,))

    dataList, nHolesRead = readPlDrillPosData.readPlDrillPosData(inFilePath, useFlat=useFlat)
    nHolesInRange = len(dataList)

    # if no data found, complain and quit
    if nHolesInRange <= 0:
        raise RuntimeError("%d holes, but none are reachable" % (nHolesRead,))

    # extract all GUIDE holes for measurement. These will
    # be measured in addition to a randomly selected subset of
    # 400 holes not of type GUIDE.
    measAllList = []
    measSubsetList = []
    for hole in dataList:
        if hole["name"] in ("GUIDE"):
            measAllList.append(hole)
        else:
            measSubsetList.append(hole)


    # select a subset of points to measure from the subset list (no GUIDE holes)
    dataArrSub = numpy.array(list((d[xType], d[yType], d["dia"]) for d in measSubsetList), dtype=float)
    # select all holes for guide
    dataArrAll = numpy.array(list((d[xType], d[yType], d["dia"]) for d in measAllList), dtype=float)
    # dataArrAll must never be empty (every plate has guide holes)...
    if len(dataArrAll) == 0:
        raise RuntimeError("No Guide Holes Found")
    if len(dataArrSub) == 0:
        # this plate contains only guide holes
        distribArr = dataArrAll
    elif len(dataArrSub) > NumHoles:
        # Select 400 points that are well distributed across the whole set
        distribPointsObj = distributePoints.DistributePoints(numToSelect = NumHoles)
        # Concatenate array containing the 400 chosen holes with the guide holes
        distPoints = distribPointsObj(dataArrSub)
        distribArr = numpy.vstack((distPoints, dataArrAll))
    else:
        # concatenate non-guide holes with guide holes
        distribArr = numpy.vstack((dataArrSub, dataArrAll))

    # order the points in a way that is efficient to measure
    orderPointsObj = orderPoints.OrderPoints(nIter=10000)
    orderedArr = orderPointsObj(distribArr)

    # create output file
    outName = "N" + str(platenum) + 'H'
    outPath = os.path.join(outDir, outName)
    # with open(outPath, "wb") as outFile:
    with open(outPath, "w") as outFile:
        # write the header
        outFile.write("#XYZ SC2" + DOSTerm)

        # write the data
        for pt in orderedArr:
            outFile.write("%11.5f %11.5f  0.0 %8.5f" % (pt[0], pt[1], pt[2]))
            outFile.write(DOSTerm)
            nHolesWritten += 1

    return genSummary.GenSummary(
        fromPath = inFilePath,
        toPath = outPath,
        nHolesRead = nHolesRead,
        nHolesInRange = nHolesInRange,
        nHolesWritten = nHolesWritten,
    )
