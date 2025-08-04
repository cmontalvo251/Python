#!/usr/bin/python

from ploteverything import *
import os
import sys
import os.path

print "Every Module Loaded Successfully"

if __name__ == "__main__":

    #Get Path from command line
    if len(sys.argv) > 1:
        inputpath = sys.argv[1]
    else:
        print "Sorry not enough input arguments"
        sys.exit()

    #In this example we will assume the naming convention for filenames and only
    #have the user set the value of the folder. We will also assume the name of the
    #folder is the date

    #1 = show plots, 0 = convert to PDF
    SHOWPLOTS = 0

    #Since this code was created on 9/9/2017 we will assume that numpitots = 4
    numPitots=4

    #We still need sigma_pitot and sigma_anemometer
    sigma_pitot = 0.03
    sigma_anemometer = 0.03
    
    quadFile = inputpath + 'ALLFILES.log'
    print 'Using Quad File = ' + quadFile
    iMetFile = inputpath + 'NOTFOUND' ##Need to change this later
    print 'Using iMet File = ' + iMetFile

    #Mesonet file is tough. We need to loop through the directory and find a file called
    #mobileusaw_*.csv
    #Pitotfile is tough as well. We need to find a file FP4V.TXT or FP4H.TXT
    mesonetFile = 'NOT FOUND'
    pitotFile = 'NOT FOUND'
    for root,dirs,files in os.walk(inputpath):
        for fname in files:
            path=os.path.join(root,fname)
            #Check for symbolic link
            if not os.path.islink(path):
                #Check for .log files
                filename, file_extension = os.path.splitext(path)

                #This checks for Mesonet File
                if file_extension == '.csv':
                    #This is either iMet or Mesonet
                    if len(fname) > 10:
                        #Check if the first 10 characters are Mesonet
                        print fname[0:10]
                        if fname[0:10] == 'mobileusaw':
                            mesonetFile = path
                #This is for FP4
                elif file_extension == '.TXT':
                    if len(fname) > 3:
                        if fname[0:3] == 'FP4':
                            pitotFile = path

    print 'Using Mesonet File = ' + mesonetFile
    print 'Using Pitot File = ' + pitotFile

    #CAL_TIMES = [25,35]
    CAL_TIMES = [-99,0]
    print 'Using CAL_TIMES = ' + str(CAL_TIMES)

    #Anemometer File is easy
    anemometerFile = inputpath + 'ANEM.TXT'

    #To get the date we need to split inputpath by / and grab the last value
    folders = inputpath.split('/')
    date = folders[len(folders)-2]

    print 'Assuming Date = ' + date

    FILES = [quadFile,iMetFile,pitotFile,mesonetFile,anemometerFile]
    do_everything(FILES,sigma_pitot,numPitots,CAL_TIMES,sigma_anemometer,SHOWPLOTS)
    
    #Rename file
    if sys.platform == 'linux2':
        os.system('cp plots.pdf ' + 'plots_' + date + '.pdf')
