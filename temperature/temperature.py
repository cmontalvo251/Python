import os
import numpy as np

class temperature():
    def __init__(self):
        self.temp = -99.0

    def update(self):
        os.system('/opt/vc/bin/vcgencmd measure_temp > file')
        fid = open('file','r')
        contents = fid.readlines()
        list_contents = contents[0].split('=')
        temp_str = list_contents[1]
        temp_str = temp_str.strip('\n')
        temp_str = temp_str.strip('C')
        temp_str = temp_str.strip("'")
        self.temp = np.float(temp_str)
        
