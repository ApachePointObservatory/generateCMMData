#!/usr/bin/env python
import sys
from generateCMMData import generate37Holes

if __name__ == "__main__":
    inFilePathList = sys.argv[1:]
    if not inFilePathList:
        print "specify file(s) to process"
        sys.exit(0)
    for inFilePath in inFilePathList:
        print "generate37Holes for inFilePath=%r" % (inFilePath,)
        generate37Holes(inFilePath, ".")
