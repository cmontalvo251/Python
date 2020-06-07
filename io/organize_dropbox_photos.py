#!/usr/bin/python

import sys
import os
#import datetime as dt
import shutil as S
import os.path
#import numpy as np

MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']

def mymove(src,dst):
    S.move(src,dst)
    outstring = 'Moving,'+src+',to,'+dst
    print outstring
    fid.write(outstring)
    fid.write('\n')
    return

def move2Desktop(fname):
    dst = '/home/carlos/Desktop/MANUAL/'+fname
    #print 'Moving File = ',src
    #print 'To = ',dst
    mymove(src,dst)
    return

if len(sys.argv) > 1:
    root_directory = sys.argv[1]
    print 'Using: ',root_directory
else:
    print 'Input Argument not given'
    sys.exit()

if not os.path.isdir('/home/carlos/Desktop/MANUAL'):
    os.makedirs('/home/carlos/Desktop/MANUAL')
    print 'Created MANUAL Directory'
else:
    print 'MANUAL directory already exists'

#Make an output file called library_roadmap
fid = open('/home/carlos/Desktop/library_roadmap','w')

for root,dirs,files in os.walk(root_directory):  
    for fname in files:
        #print fname
        path=os.path.join(root,fname)
        src = path
        #print path
        #Parse path by the extension
        filename, file_extension = os.path.splitext(fname)
        #print file_extension
        if file_extension == '.mp4':
            move2Desktop(fname)
        else:
            try:
                ymd = path.split('-')
                month = int(ymd[1])
                #print month
                #print MONTHS[month-1]
                dst = '/home/carlos/Desktop/'+MONTHS[month-1]+'/'+fname
                try:
                    mymove(src,dst)
                except:
                    dir_ = '/home/carlos/Desktop/'+MONTHS[month-1] 
                    os.makedirs(dir_)
                    mymove(src,dst)
                    print 'Last one did not work'
            except:
                move2Desktop(fname)

fid.close()
