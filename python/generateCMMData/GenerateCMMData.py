#!/usr/local/bin/python
"""
Generates CMM data (for the UW Brown and Sharp CMM running Avail) from SDSS "plDrillPos" files,
as follows:
- Creates a new folder whose name includes the range of files processed
- Creates N#### files containing a small sampling of holes per plate; all plates are tested at this level
- Creates N####A files containing all reachable holes; a few plates are tested at this level

History
2002-01-25 ROwen    First version with history;
    bug fix: new subdirectory path had a minor bug that showed up under unix but not Mac OS;
    mod. to get year and month for subdir name from creation date of first file in list.
2003-04-15 ROwen    Modified to use RO.procFiles.
2005-03-15 ROwen    Removed ancient commented-out code to generate a file copy batch job.
2010-06-16 ROwen    Version 2.0:
                    - Made debug mode explicit.
                    - Modified to not use RO.procFiles.
2010-06-24 ROwen    Version 2.1:
                    - Handle modern plDrillPos files with zDrill field (and older files without)
"""

import os
import os.path
import sys
import time
import re
import Generate37Holes
import GenerateAllHoles

DOSTerm = "\r\n"
Debug = False

__version__ = "2.1"

FileNumberRE = re.compile(r'plDrillPos-(\d\d\d\d)\.par$')

def fileNameToPlateNum(filePath):
    """Parses a file path whose file name is of the form 'plDrillPos-####.par',
    where #### is the plate number, and returns the plate number as a string.
    """
    fileName = os.path.basename(filePath)
    fnumMatch = FileNumberRE.match(fileName)
    if not fnumMatch:
        raise RuntimeError, "cannot parse file name :%s:" % (fileName,)
    return fnumMatch.group(1)
    
def run(filePathList):
    if not filePathList:
        print "No files to process; nothing done."
        return
    
    # generate list of plate numbers
    fileNumList = [fileNameToPlateNum(filePath) for filePath in filePathList]
    fileNumList.sort()
    
    # generate output directory (dies if it already exists)
    # as a subdirectory of the location of the first input file
    inDir = os.path.dirname(filePathList[0])
    fileCreationTime = os.stat(filePathList[0])[9]
    year, month = time.localtime(fileCreationTime)[0:2]
    subdirName = "%s-%s %4d-%02d" % (fileNumList[0], fileNumList[-1], year, month)
    outDir = os.path.join(inDir, subdirName)
    print "\nCreating output directory %r\n" % (outDir)
    os.mkdir(outDir)

    # process the files 
    print "\nGenerating files for measuring 37 holes\n"
    Generate37Holes.run(filePathList, outDir)
    print "\nGenerating files for measuring all holes\n"
    GenerateAllHoles.run(filePathList, outDir)

    print "\nConvert more plDrillPos-xxxx.par files by droppping them on the application icon\n\n"

if __name__ == "__main__":
    if Debug:
        print "Running in debug mode"
        filePathList = ["plDrillPos-0825.par", "plDrillPos-0832.par"]
    else:
        filePathList = sys.argv[1:]

    run(filePathList)
