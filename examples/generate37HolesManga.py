#!/usr/bin/env python
import os.path
from generateCMMData import generate37Holes

if __name__ == "__main__":
    inputDir = os.path.join(os.path.dirname(__file__))
    inputFiles = ["plDrillPos-7341.par", "plDrillPos-7342.par", "plDrillPos-7343.par", "plDrillPos-4100.par"]
    for f in inputFiles:
        generate37Holes(os.path.join(inputDir, f), inputDir)

