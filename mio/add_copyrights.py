#!/usr/bin/python

import sys
import os
import os.path
from shutil import *

def git_files(ifile):
    iterable = ['FAQ','COPYING','README','MANIFEST','exclude','master','HEAD','config','COMMIT_EDITMSG','description','index','octave-workspace']
    for element in iterable:
        if element == ifile:
            return True
    return False

for root,dirs,files in os.walk('.'):
    for ifile in files:
        #Make sure it's not this file
        if ifile[-1] == "~":
            print "Removing file = ",ifile
            src = os.path.join(root,ifile)
            os.remove(src)
        if ifile != 'add_copyrights.py' and ifile[-1] != "~" and root[2:6] != '.git':
            #Ok first we need to see what file extension the file has
            filename, ext = os.path.splitext(ifile)
            comment = 'skip'
            if ext == '.m' or ext == '.bib' or ext == '.tex':
                comment = '%'
            elif ext == '.txt':
                comment = ''
            elif ext == '.bat':
                comment = 'REM'
            elif ext == '.f' or ext == '.f90' or ext == '.f95':
                comment = '!'
            elif ext == '.cpp' or ext == '.c' or ext == '.h':
                comment = '//'
            elif ext == '.py' or ext == '.sh' or ext == '':
                #Watch out for git files
                if not git_files(ifile):
                    comment = '#'
                
                
            #Skipping Files = pdf,dll,exe,mp3,ins,cls,bst,eps,dtx,sample,stl,STL,backup,pyc,png,exe
                
            if comment != 'skip' and comment == '#':
                src = os.path.join(root,ifile)
                print "File = ",src,"--- Extension = ",ext,"--- Comment = ",comment
                copyrightstring = ["Copyright - Carlos Montalvo 2015\n","You may freely distribute this file but please keep my name in here\n","as the original owner\n"]
                fid = open(src,"a")
                fid.write("\n")
                for s in copyrightstring:
                    fid.write(comment+' '+s)
                fid.close()
            else:
                # print 'Skipping File = ',ifile
                c = 2


#Copyright - Carlos Montalvo 2015
#You may freely distribute this file but please keep my name in here 
#as the original owner
