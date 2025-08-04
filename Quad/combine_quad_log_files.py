#!/usr/bin/python

import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import DateFormatter
import numpy as np
from pdf import *
import sys
import os
import datetime as dt
from shutil import *
import os.path

if __name__ == "__main__":

    #Get Path from command line
    if len(sys.argv) > 1:
        inputpath = sys.argv[1]
    else:
        print "Sorry not enough input arguments, Need folder location of .log"
        sys.exit()

    ##Delete ALLFILES.log if it exists
    ALLFILES = inputpath+"ALLFILES.log"
    if os.path.isfile(ALLFILES):
        print "Removing ALLFILES.log"
        os.remove(ALLFILES)

    #Now open file for writing
    outfile = open(ALLFILES,'w')

    logfiles = []

    for root,dirs,files in os.walk(inputpath):
        for fname in files:
            path=os.path.join(root,fname)
            #Check for symbolic link
            if not os.path.islink(path):
                #Check for .log files
                filename, file_extension = os.path.splitext(path)
		if file_extension == '.log' or file_extension == '.LOG':
                    if path != ALLFILES:
                        logfiles.append(path)

    sorted_logfiles = sorted(logfiles)

    #Sort the files
    for filename in sorted_logfiles:
        print "Exporting File = ",filename
        file = open(filename)
        for line in file:
            outfile.write(line)

    #close file
    outfile.close()

    
                    
                    
                    
                

