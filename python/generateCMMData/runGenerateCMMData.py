#!/usr/bin/env python
"""
Run GenerateCmmData script

History
2010-06-18 ROwen
"""
import sys
import RO.Wdg
import GenerateCMMData # so py2app can find the script and its dependencies

initialText = "Generate CMM Data %s\n\n" % (GenerateCMMData.__version__)
if len(sys.argv) < 3:
    initialText += "Convert plDrillPos-xxxx.par files by droppping them on the application icon\n\n"

RO.Wdg.DropletRunner("GenerateCMMData.py", initialText=initialText, height=50)
