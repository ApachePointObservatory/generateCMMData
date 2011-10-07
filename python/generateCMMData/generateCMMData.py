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
2011-10-07 ROwen    Version 2.2:
                    - Use RO.Wdg.DropletApp; output files are put in the same directory as input files.
"""
import os.path
import RO.Wdg
import generate37Holes
import generateAllHoles

__version__ = "2.2"

class GenerateCMMDataWdg(RO.Wdg.DropletApp):
    """Convert plDrillPos files to CMM "N" files
    """
    def __init__(self, master, filePathList=None):
        """Construct a GenerateCMMData
        
        Inputs:
        - master: master widget; should be root
        - filePathList: list of files to process
        """
        RO.Wdg.DropletApp.__init__(self,
            master = master,
            width = 135,
            height = 20,
            recursionDepth = 1,
            patterns = "plDrillPos*.par",
            exclDirPatterns = ".*",
        )
        
        self.logWdg.addMsg("""GenerateCMMData version %s""" % (__version__,))
        
        if filePathList:
            self.processFileList(filePathList)

    def processFile(self, filePath):
        """Process one plDrillPos file.
        """
        outDir, fileName = os.path.split(filePath)
        self.logWdg.addMsg("Processing %s" % (fileName,))
        generate37Holes.runOneFile(filePath, outDir)
        generateAllHoles.runOneFile(filePath, outDir)
    

if __name__ == "__main__":
    import sys
    import Tkinter
    filePathList = sys.argv[1:]
    # strip first argument if it starts with "-", as happens when run as a Mac application
    if filePathList and filePathList[0].startswith("-"):
        filePathList = filePathList[1:]

    root = Tkinter.Tk()
    root.title("GenerateCMMData")
    
    fitPlugPlateWdg = GenerateCMMDataWdg(master=root, filePathList=filePathList)
    fitPlugPlateWdg.pack(side="left", expand=True, fill="both")
    root.mainloop()
