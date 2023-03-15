#!/usr/bin/python

import os

def getlines(fullpath):
    length = 0
    file = open(fullpath)
    for line in file:
        length+=1
    file.close()
    print(fullpath,'LINES = ',length)
    return length

length = 0
for root,dirs,files in os.walk('./'):
    for fname in files:
        filename, ext = os.path.splitext(fname)
        if ext == '.cpp' or ext == '.h' or ext == '.hpp' or ext == '.c' or ext == '.py' or ext == '.m':
            fullpath = root + '/' + fname
            length += getlines(fullpath)
print('TOTAL = ',length)

