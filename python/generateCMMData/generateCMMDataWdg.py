import os.path
import RO.Wdg
from .generate37Holes import generate37Holes
from . import generateAllHoles
from . import version

__all__ = ["GenerateCMMDataWdg"]

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
            width = 65,
            height = 40,
            recursionDepth = 1,
            patterns = "plDrillPos*.par",
            exclDirPatterns = ".*",
        )
        
        self.logWdg.addMsg("""GenerateCMMData version %s""" % (version.__version__,))
        
        if filePathList:
            self.processFileList(filePathList)

    def processFile(self, filePath):
        """Process one plDrillPos file.
        """
        outDir, fileName = os.path.split(filePath)
        self.logWdg.addMsg("Processing %s" % (fileName,))
        res = generate37Holes(filePath, outDir)
        self.logWdg.addMsg("Wrote %7s: %4d holes read; %4d in range; %4d written" % \
            (os.path.basename(res.toPath), res.nHolesRead, res.nHolesInRange, res.nHolesWritten))
        
        res = generateAllHoles(filePath, outDir)
        self.logWdg.addMsg("Wrote %7s: %4d holes read; %4d in range; %4d written" % \
            (os.path.basename(res.toPath), res.nHolesRead, res.nHolesInRange, res.nHolesWritten))
        
