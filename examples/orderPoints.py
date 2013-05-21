#!/usr/bin/env python
import sys
import matplotlib.pyplot as pyplot
import generateCMMData.testData as testData
from generateCMMData.orderPoints import OrderPoints

if __name__ == "__main__":
    dataArr = testData.getAllPoints()

    op = OrderPoints(nIter=50000, nToPrint=10)
    orderedPoints = op(dataArr)
    pyplot.plot(orderedPoints[:,0], orderedPoints[:,1])
    pyplot.show()
