#!/usr/bin/python

import sys
import os
import os.path
from shutil import *

for root,dirs,files in os.walk('.'):
    for src in files:
        print "Current File = ",src
        if src.find(':') != -1:
            dst = src.replace(":","_")
        else:
            dst = src
        try:
            copyfile(src,dst)
            os.remove(src)
            print "Changing to....",dst
        except:
            print "Skipping File"

# Copyright - Carlos Montalvo 2015
# You may freely distribute this file but please keep my name in here
# as the original owner
