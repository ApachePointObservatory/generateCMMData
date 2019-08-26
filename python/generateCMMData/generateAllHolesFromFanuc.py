#!/usr/bin/env python

"""
Generate data for the UW Brown and Sharp CMM from SDSS "plFaunic" files (which are used by the mill).

Choose all reachable holes and order them for efficient measuring.

History
2014-01-21 CS       Inintial Creation
"""
import os.path
import re
import numpy
from . import genSummary
from . import orderPoints

__all__ = ["generateAllHolesFromFanuc"]

DOSTerm = "\r\n"
MMPerInch = 25.4

def readPlFanucDrillPosData(inFilePath):
    """Read data from a plFanuc file

    Inputs:
    - inFilePath: path to file containing hole position data

    Return:
    - dataList: sequence of dictionaries with keys: x, y, dia, name. No bounds checking is done.
    """
    dataList = []
    parseMe = False
    with file(inFilePath, "rU") as inFile:
        for line in inFile:
            line = line.strip()
            if parseMe and line.startswith("G60"):
                # parse it
                posDict = {}
                for piece in line.split()[1:3]: # just get x and y
                    if piece.startswith("X"):
                        posDict["xPos"] = float(piece[1:])*MMPerInch
                    else:
                        assert piece.startswith("Y")
                        posDict["yPos"] = float(piece[1:])*MMPerInch
                # hardcode the diameter
                posDict["dia"] = 2.16662
                dataList.append(posDict)

            elif line.startswith("M08"):
                # beging recording positions
                # M08 signals coolant on
                # holes which follow are science holes
                # drilled first
                parseMe = True

            elif line.startswith("M09"):
                # coolant off, science holes done
                break

    return dataList

def generateAllHolesFromFanuc(inFilePath, outDir):
    """Generate one CMM file with all reachable holes from a plFaunic*.par file.

    Return a GenSummary object describing what was done.
    """
    nHolesWritten = 0

    inName = os.path.basename(inFilePath)

    # extract plate number from file name
    try:
        platenum = int(re.split("[-.]", inName)[1])
    except:
        raise RuntimeError("cannot parse file name: %s" % (inName,))

    dataList = readPlFanucDrillPosData(inFilePath)
    # nHolesInRange = len(dataList)

    # # if no data found, complain and quit
    # if nHolesInRange <= 0:
    #     raise RuntimeError("%d holes, but none are reachable" % (nHolesRead,))

    dataArr = numpy.array(list((d["xPos"], d["yPos"], d["dia"]) for d in dataList), dtype=float)

    # order the points in a way that is efficient to measure
    # orderPointsObj = orderPoints.OrderPoints(nIter=50000)
    # orderedArr = orderPointsObj(dataArr)
    orderedArr = dataArr

    # create output file
    outName = "N" + str(platenum) + "A"
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
        nHolesRead = len(dataArr),
        nHolesInRange = len(dataArr),
        nHolesWritten = nHolesWritten,
    )
