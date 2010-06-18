Generating Hole Position Data for the CMM in the UW Machine Shop

Obtain the plDrillPos files for the desired plates.

Select all of the plDrillPos files you want to convert (typically all in a folder) onto the program "GenerateCMMData". Warning: drag the files themselves, do NOT drag folders.

GenerateCMMData will create a new folder (inside the current folder) containing all the necessary files, including "filecp" and a N### and N###A data file for each plate. The folder will be called ####-#### yyyy-mm (plug_plate_#-plug_plate_# year-month).





The format for CMM hole position data files is as follows:

The file must have DOS line endings ("\r\n")

The first line must be:
#XYZ SC2

The rest of the file is data, one entry per hole, space-separated data:
x   y   0.0  diameter (all in mm)

Example:
#XYZ SC2
0.00000        0.00000   0.0   3.175
150.07844   -259.94614   0.0   2.16662
-150.07844  -259.94614   0.0   2.16662
-300.15942     0.00000   0.0   2.16662
-150.07844   259.94614   0.0   2.16662
150.07844    259.94614   0.0   2.16662
300.15942      0.00000   0.0   2.16662
0.00000        0.00000   0.0   2.16662
316.75745    182.88000   0.0   6.350
-316.75745   182.88000   0.0   6.350


Russell Owen
2010-06-18

