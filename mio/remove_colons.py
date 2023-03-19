#!/usr/bin/python

import sys
import os
import os.path
from shutil import *

for root,dirs,files in os.walk('.'):
    for src in files:
        if src.find(':') != -1:
            dst = src.replace(":","_")
            fullsrc = root + '/' + src
            fulldst = root + '/' + dst
            print "Current File = ",fullsrc
            copyfile(fullsrc,fulldst)
            os.remove(fullsrc)
            print "Changing to....",fulldst

# Copyright - Carlos Montalvo 2015
# You may freely distribute this file but please keep my name in here
# as the original owner
