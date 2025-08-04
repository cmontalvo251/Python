#!/usr/bin/python

import sys
import os
import datetime as dt
from shutil import *
import os.path
#import os.mkdir

if __name__ == "__main__":

    #Get Path from command line
    if len(sys.argv) > 3:
        inputpath = sys.argv[1]
        IN_MONTH = float(sys.argv[2])
        IN_DAY = float(sys.argv[3])
        print IN_MONTH,IN_DAY
    else:
        print "Sorry not enough input arguments, folder name, month, day"
        sys.exit()

    #Let's make a backup FOLDER for caroline
    backup_folder = 'BACKUP_CAROLINE_DO_NOT_DELETE_THIS_FOLDER/'
    try:
        os.mkdir(backup_folder)
    except:
        print 'Skipping making backup directory'
        
    #inputpath is now the name of the directory
    for root,dirs,files in os.walk(inputpath):
        for fname in files:
            path=os.path.join(root,fname)
            #Check for symbolic link
            if not os.path.islink(path):
                #Check for .log files
                filename, file_extension = os.path.splitext(path)
                endoffile = filename[len(filename)-7:len(filename)]
                print filename
                #print endoffile
		if file_extension == '.csv' and endoffile != "_edited":
                    infile = open(path)

                    #Now open file for writing
                    infilename, file_extension = os.path.splitext(filename)

                    src = path
                    dst = backup_folder + fname
                    copyfile(src,dst)
                    
                    outfilename = infilename + "_edited.csv"
                    #print outfilename
                    outfile = open(str(outfilename),'w')

                    #Default to 6
                    column = 6
                    for line in infile:
                        if len(line) > 2:
                            data = line.split(',')
                            if data[0] == "Time":
                                column = 40
                            if data[0] != "Time":
                                date = data[column]
                                ymd = date.split('/')
                                #It's possible here that ymd is not an integer.
                                #Not sure how that could happen.
                                #Will have to look at data from caroline when she sends it
                                if float(ymd[0]) == 2017:
                                    if float(ymd[1]) == IN_MONTH:
                                        if float(ymd[2]) == IN_DAY:
                                            #print ymd
                                            outfile.write(line)
                

                    #close file
                    outfile.close()

    
                    
                    
                    
                

