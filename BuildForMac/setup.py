from __future__ import with_statement
"""The Python portion of the script that builds GenerateCMMData

Usage:
% python setup.py [--quiet] py2app

History:
2010-06-14 ROwen
"""
import os
import shutil
import subprocess
import sys
from setuptools import setup

# add various bits to the path
pkgRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.isfile("extraPaths.txt"):
    with file("extraPaths.txt") as pathFile:
        pathList = [pkgRoot]
        for pathStr in pathFile:
            pathStr = pathStr.strip()
            if not pathStr or pathStr.startswith("#"):
                continue
            pathList.append(pathStr)
sys.path = pathList + sys.path

import GenerateCMMData

appName = "GenerateCMMData"
mainScript = "GenerateCMMData.py"
mainProg = os.path.join(pkgRoot, "runGenerateCMMData.py")
appPath = os.path.join("dist", appName + ".app")
iconFile = "%s.icns" % appName
versStr = GenerateCMMData.__version__

inclModules = (
)
# packages to include recursively
inclPackages = (
#    "RO",
)

# see plistlib for more info
plist = dict(
    CFBundleName                = appName,
    CFBundleExecutable          = appName,
    CFBundleShortVersionString  = versStr,
    CFBundleGetInfoString       = "%s %s" % (appName, versStr),
    CFBundleDocumentTypes       = [
        dict(
            CFBundleTypeName = "TEXT",
            CFBundleTypeRole = "Viewer",
            LSItemContentTypes = [
                "public.plain-text",
                "public.text",
                "public.data",
                "com.apple.application-bundle",
            ],
        ),
    ],
)

setup(
    app = [mainProg],
    setup_requires = ["py2app"],
    options = dict(
        py2app = dict (
            plist = plist,
            iconfile = iconFile,
            includes = inclModules,
            packages = inclPackages,
        )
    ),
)

shutil.copy(
    os.path.join(pkgRoot, mainScript),
    os.path.join(appPath, "Contents", "Resources"),
)

print "*** Creating disk image ***"
appName = "%s_%s_Mac" % (appName, versStr)
destFile = os.path.join("dist", appName)
args=("hdiutil", "create", "-srcdir", appPath, destFile)
retCode = subprocess.call(args=args)
