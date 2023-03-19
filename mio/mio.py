import numpy as np

##In order to import this toolbox into a python script you need to 
##do the following. Copy the following lines of code below
# import sys
# sys.path.append('/home/carlos/Dropbox/BlackBox/plotting')
# from plotting import *

# or

# In order to get python to search for all of your lovely blackbox 
# python routines. Add this to your .bashrc file

# for d in /home/carlos/Dropbox/BlackBox/*/; do
# 	PYTHONPATH+=:$d
# done
# export PYTHONPATH

# For Thonny make symbolic links here
# ~/.thonny/BundledPython36/lib/python3.6/site-packages$

def loadtxt(filename,delimiter=' '):
    try:
        file_ID = open(filename)
    except:
        print(filename,"Does Not Exist")
        return None;
    file_ID.close()
    print("Successfully Opened File = ",filename)
    try:
        data_np = np.loadtxt(filename)
        print('(Rows,Cols) = ',np.shape(data_np))
        return data_np
    except ValueError:
        print('Numpy Loadtxt returned a ValueError. Trying with line in file loop')
        file = open(filename)
        mat = []
        for line in file:
            row = line.split(delimiter)
            vec = []
            for r in row:
                try:
                    vec.append(np.float(r))
                except ValueError:
                    if len(r) > 0:
                        if ord(r) != 10:
                            print('Value Cannot Be Converted to Float: ',ascii(r),' ASCII: ',ord(r))
            mat.append(vec)
        data = np.array(mat)
        print('Line in File FTW')
        print('(Rows,Cols) = ',np.shape(data))
        return data

def dlmread(filename,delimiter=',',suppressWarnings=False,variableLength=False):

    try:
        file_ID = open(filename)
    except:
        if suppressWarnings == False:
            print(filename,"Does Not Exist")
        return None;

    maxlength = 0
    if variableLength == True:
        #We need to loop through the file and figure out the maximum number of columns
        for line in file_ID:
            row = line.split(delimiter)
            #Remove the line endings
            try:
                row.remove('\n')
            except:
                pass
            if len(row) > maxlength:
                maxlength = len(row)
        #//Close the file and then
        file_ID.close()
        #re open it 
        file_ID = open(filename)
        print('Max Width of File = ' + str(maxlength))
    
    if 1: ##Wha? Why is this here? ***facepalm***
        print("Successfully Opened File = ",filename)
        data = []
        ctr = -1
        for line in file_ID:
            ctr+=1
            #Ok so if the delimiter is a space sometimes fortran is wierd and has a ton of spaces
            #so we need something more robust -- so for FORTRAN we will add a try catch statement below
            row = line.split(delimiter)
            row_np = []
            for x in row:
                try:
                    val = np.float(x)
                    row_np.append(val)
                except:
                    val = []
                    #print 'x=',x
            # if len(row_np) != 35:
            #     print 'line=',line
            #     print 'row =',row
            #     print 'row_np=',row_np,len(row_np)
            if len(row_np) > 0:
                if (variableLength == True):
                        while len(row_np) < maxlength:
                            #Pad vector with zeros
                            row_np.append(0)
                #print row_np,len(row_np)
                data.append(np.asarray(row_np))
            
        data_np = np.asarray(data)
        print('(Rows,Cols) = ',np.shape(data_np))
        return data_np

##Added this routine to outut arrays to files
def dlmwrite(outfilename,outarray):
    #Output Contents to File
    try:
        [r,c] = np.shape(outarray)
    except:
        r = np.shape(outarray)[0]
        c = -1
    outfile = open(outfilename,'w')
    for x in range(0,r):
        if c != -1:
            out = outarray[x,:]
            list = out.tolist()
            s = " ".join(map(str,list))
        else:
            #1D array
            s = str(outarray[x])
        outfile.write(s+'\n')
    outfile.close()
    
# Copyright - Carlos Montalvo 2017
# You may freely distribute this file but please keep my name in here
# as the original owner
