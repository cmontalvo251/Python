import numpy as np
import re

import fuzzywuzzy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

fid = open('RSAP_2022_Student_list.csv')
ctr = 0
names = []
for line in fid:
    #print(line)
    row = line.split(',')
    if ctr != 0:
        first_name = row[0]
        last_name = row[2]
        names.append(first_name + ' ' + last_name)        
    ctr+=1
    
fid = open('RSAP_Tuesday_Week_2.csv')
ctr = 0
name_2 = []
for line in fid:
    #print(line)
    row = line.split(',')
    if ctr > 2:
        name_2.append(row[1])        
    ctr+=1
    
for main_name in names:
    ##Find the closest match
    max_ratio = 0.0
    for name in name_2:
        ratio = fuzz.ratio(main_name.lower(), name.lower())
        if ratio > max_ratio:
            max_ratio = ratio
            matching_name = name
    print('Matched Name ',main_name,' to ',matching_name,': ',max_ratio)
    
