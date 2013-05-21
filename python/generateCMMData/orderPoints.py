import math
import numpy
import random

from . import anneal

class OrderPoints(object):
    """Place a set of points on a plane in an order in which they can be traversed quickly.
    
    The list always starts with the point nearest the center,
    so that the CMM starts moving more predictably and to discourage raster order
    (which could cause odd errors if the temperature changed during measurement).
    
    To use:
    - Construct a OrderPoints
    - Call the object as a function with your list of points
    
    Credits:
    Thanks to Richard J. Wagner for the simulated annealing code
    """
    def __init__(self, nIter=5000, minTemp=1.0e-9, nToPrint=0):
        """Construct a OrderPoints
        
        Inputs
        - nIter: number of iterations of the simulated annealer
        - minTemp: minimum temperature of the simulated annealer; the results seem fairly insensitive
            to this value as long as it is small enough
        - nToPrint: number of intermediate results from the simulated annealer to print to stdout
        """
        self.nIter = int(nIter)
        self.minTemp = float(minTemp)
        self.nToPrint = int(nToPrint)
                
    def computeEnergy(self, xyPoints):
        """Compute the energy of a set of points
        """
        # cost = max(dx, dy); this is the best match for a machine such as the CMM
        # (assuming the x and y axes have the same velocity limit)
        return numpy.sum(numpy.sqrt(numpy.max(numpy.abs(xyPoints[:-1, 0:2] - xyPoints[1:, 0:2]), 1)))

        # cost = Euclidean distance; this works well enough for a machine,
        # but over-estimates the time required for a diagonal move
#        return numpy.sum(numpy.sqrt(numpy.sum(numpy.square(xyPoints[:-1, 0:2] - xyPoints[1:, 0:2]), 1)))
        
    def changeState(self, xyPoints):
        """Change the state of xyPoints in place.
        
        Randomly swap two points
        """
        nPts = len(xyPoints)
        ind0 = random.randint(1, nPts-1)
        ind1 = random.randint(1, nPts-1)
        while ind1 == ind0:
            ind1 = random.randint(1, nPts-1)
        # make copy of the sources to make sure the swap works correctly
        xyPoints[ind0], xyPoints[ind1] = tuple(xyPoints[ind1]), tuple(xyPoints[ind0])

    def __call__(self, xyPoints):
        """Reorder the points in xyPoints to make a short path from the first to the last.
        
        Inputs:
        - xyPoints: a set of (x, y, ...?) data where x, y are positions on a plane
        """
        numPoints = len(xyPoints)
        initialXYPoints = numpy.array(xyPoints, dtype=float, copy=True)

        # find point closest to center and start with that
        minInd = numpy.argmin(numpy.sum(numpy.square(initialXYPoints[:]), 1))
        if minInd != 0:
            initialXYPoints[0], initialXYPoints[minInd] = tuple(initialXYPoints[minInd]), tuple(initialXYPoints[0])
        initialEnergy = self.computeEnergy(initialXYPoints)
        
        annealer = anneal.Annealer(self.computeEnergy, self.changeState)
        xyPoints = annealer.anneal(initialXYPoints, initialEnergy, self.minTemp, self.nIter, self.nToPrint)[0]
        return xyPoints
