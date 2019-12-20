#!/bin/bash

import numpy as np

#Time since Jun 2 at Midnight
seconds = 245463.0
minutes = seconds/60.0
hours = minutes/60.0
days = np.floor(hours/24.0)

hours = np.floor(hours - days*24.0)

minutes = np.floor(minutes - hours*60.0 - days*24.0*60.0)

seconds = np.floor(seconds - minutes*60.0 - hours*60.0*60.0 - days*24.0*60.0*60.0)

print 'Day = ',2+days
print 'Month = ','June'
print 'Hour = ',hours-5-12
print 'Minute = ',minutes
print 'Second = ',seconds







