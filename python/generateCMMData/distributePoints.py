import sys
import random
import numpy
import anneal

class DistributePoints(object):
    """Select a small set of points that are as evenly and widely distributed on a plane.
    
    To use:
    - Construct a DistributePoints
    - Call the object as a function with your list of points
    
    Credits:
    Thanks to Richard J. Wagner for the simulated annealing code
    """
    def __init__(self, numToSelect=37, nIter=1000, minTemp=1.0e-6, nToPrint=0):
        """Construct a DistributePoints
        
        Inputs
        - numToSelect: number of points to select from xyPoints
        - nIter: number of iterations of the simulated annealer
        - minTemp: minimum temperature of the simulated annealer; the results seem fairly insensitive
            to this value as long as it is small enough
        - nToPrint: number of intermediate results from the simulated annealer to print to stdout
        """
        self.numToSelect = int(numToSelect)
        self.nIter = int(nIter)
        self.minTemp = float(minTemp)
        self.nToPrint = int(nToPrint)
                
        pt0IndexList = []
        pt1IndexList = []
        for i in range(self.numToSelect):
            for j in range(i + 1, self.numToSelect):
                pt0IndexList.append(i)
                pt1IndexList.append(j)
        self.pt0IndexArr = numpy.array(pt0IndexList, dtype=int)
        self.pt1IndexArr = numpy.array(pt1IndexList, dtype=int)

    def computeEnergy(self, xyPoints):
        """Compute the energy of a set of points
        
        Note: uses only the first self.numToSelect points
        """
        return 1000 * numpy.sum(1.0 / numpy.sum(numpy.square(
            xyPoints[self.pt0IndexArr, 0:2] - xyPoints[self.pt1IndexArr, 0:2]
        ), 1))
        
    def changeState(self, xyPoints):
        """Change the state of xyPoints in place.
        
        Randomly swap two points, one in range 0:self.numToSelect, the other past that
        """
        selInd = random.randint(0, self.numToSelect-1)
        remInd = random.randint(self.numToSelect, len(xyPoints) - 1)
        xyPoints[selInd], xyPoints[remInd] = xyPoints[remInd], xyPoints[selInd]

    def __call__(self, xyPoints, doTrim=True):
        """Select self.numToSelect points from self.xyPoints distributed as far apart as possible.
        
        Inputs:
        - xyPoints: a set of (x, y, ...?) data where x, y are positions on a plane
        - doTrim: if True (default) return the points to measure; if False then return all points
        """
        numPoints = len(xyPoints)
        if numPoints <= self.numToSelect:
            raise RuntimeError("number of points = %s <= %s = numToSelect" % \
                (numPoints, self.numToSelect))
        initialXYPoints = numpy.array(xyPoints, dtype=float, copy=True)

        numpy.random.shuffle(initialXYPoints)
        initialEnergy = self.computeEnergy(initialXYPoints)
        
        annealer = anneal.Annealer(self.computeEnergy, self.changeState)
        xyPoints = annealer.anneal(initialXYPoints, initialEnergy, self.minTemp, self.nIter, self.nToPrint)[0]
        if doTrim:
            return xyPoints[0:self.numToSelect]
        else:
            return xyPoints
        

if __name__ == "__main__":
    from . import testData

    try:
        import matplotlib.pyplot as pyplot
    except ImportError:
        pyplot = None
        print "Cannot find matplotlib.pyplot so no plot will be shown"

    testPoints = testData.getAllPoints()
    dp = DistributePoints()
    state = dp(testPoints, doTrim=False)
    print "final energy=", dp.computeEnergy(state)
    if pyplot:
        pyplot.plot(state[dp.numToSelect:,0], state[dp.numToSelect:,1], 'bo')
        pyplot.plot(state[:dp.numToSelect,0], state[:dp.numToSelect,1], 'ro')
        pyplot.show()
