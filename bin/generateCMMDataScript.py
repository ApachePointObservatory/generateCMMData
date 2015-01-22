#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
import argparse
import os
import glob
import datetime
import shutil

from generateCMMData import generate37Holes, generateAllHoles, generateAllHolesFromFanuc

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Script to convert plDrillPos files into CMM measurement files")
    parser.add_argument('path', type=str,
                        help='a path to a directory or plDrillPos/fanuc file. If directory, all plDrillPos/fanuc files within that directory are converted.')
    parser.add_argument('--focal', action="store_true", help="if specified, measure focal x,y positions, else measure flat x,y positions.")
    parser.add_argument('--fanuc', action="store_true", help="if specified, parse fanuc files rather than plDrillPos.")

    args = parser.parse_args()
    absPath = os.path.abspath(args.path)
    if os.path.isdir(absPath):
        # grab all drill files for conversion
        basePath = absPath
        globStr = os.path.join(absPath, "plFanuc*.par" if args.fanuc else "plDrillPos*.par")
        fileList = glob.glob(globStr)
    else:
        # verify a file was passed and it has the right name
        basePath, fileName = os.path.split(absPath)
        if not fileName.startswith("plFanuc" if args.fanuc else "plDrillPos"):
            raise RuntimeError("%s is not a %s file!"%(fileName, "plFanuc" if args.fanuc else "plDrillPos"))
        fileList = [fileName]
    useFlat = not args.focal
    plateNums = []
    for f in fileList:
        print("Processing %s" % (f,))
        plateNums.append(int(f.split("-")[1].split(".")[0]))
        if args.fanuc:
            res = generateAllHolesFromFanuc(f, basePath)
            print("Wrote %7s: %4d holes read; %4d in range; %4d written" % \
                (os.path.basename(res.toPath), res.nHolesRead, res.nHolesInRange, res.nHolesWritten))
        else:
            res = generate37Holes(f, basePath, useFlat)
            print("Wrote %7s: %4d holes read; %4d in range; %4d written" % \
                (os.path.basename(res.toPath), res.nHolesRead, res.nHolesInRange, res.nHolesWritten))

            res = generateAllHoles(f, basePath, useFlat)
            print("Wrote %7s: %4d holes read; %4d in range; %4d written" % \
                (os.path.basename(res.toPath), res.nHolesRead, res.nHolesInRange, res.nHolesWritten))
        # create directories and move files there
    minNum = min(plateNums)
    maxNum = max(plateNums)
    datestr = datetime.datetime.now().strftime("%Y-%M")
    dirName = "%i-%i %s"%(minNum, maxNum, datestr)
    pathToHolePos = "/nfsmount/shopdc0/Hole position files"
    newDir = os.path.join(pathToHolePos, dirName)
    assert os.path.exists(pathToHolePos)
    os.mkdir(newDir)
    # get all the files we just created
    nFiles = glob.glob("N*")
    for f in nFiles:
        shutil.copy(f, newDir)



