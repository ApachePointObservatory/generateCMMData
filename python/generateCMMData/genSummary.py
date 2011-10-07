#!/usr/bin/env python
"""Summary of results from a hole generator

History
2011-10-06 ROwen
"""
import RO.Constants

class GenSummary(object):
    def __init__(self, fromPath, toPath, nHolesRead, nHolesInRange, nHolesWritten):
        self.fromPath = fromPath
        self.toPath = toPath
        self.nHolesRead = nHolesRead
        self.nHolesInRange = nHolesInRange
        self.nHolesWritten = nHolesWritten
