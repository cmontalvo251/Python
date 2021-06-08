import sys, time

import navio.rcinput
import navio.util

navio.util.check_apm()

rcin = navio.rcinput.RCInput()
i = 0
num_channels = 9

while (True):
    period = []
    for i in range(num_channels):

        value = rcin.read(i)
        period.append(value)
        
    print period
    #time.sleep(1)
