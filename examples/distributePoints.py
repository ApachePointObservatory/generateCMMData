#!/usr/bin/env python
import sys
import matplotlib.pyplot as pyplot
import generateCMMData.testData as testData
from generateCMMData.distributePoints import DistributePoints

if __name__ == "__main__":
    testPoints = testData.getAllPoints()
    dp = DistributePoints(nIter=50000, nToPrint=10)
    state = dp(testPoints, doTrim=False)
    print "final energy=", dp.computeEnergy(state)

    pyplot.plot(state[dp.numToSelect:,0], state[dp.numToSelect:,1], 'bo')
    pyplot.plot(state[:dp.numToSelect,0], state[:dp.numToSelect,1], 'ro')
    pyplot.show()
