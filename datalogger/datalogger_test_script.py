##Include the datalogger class
from datalogger import *
#Creating a variable called Datalogger. just like int or double I can do Datalogger
logger = Datalogger()

#Get a Timer
import time

##In order to do input arguments you need sys
import sys

print("Running Datalogger Test Script \n")

#Looked for the FIle
print("Looking for File in " + sys.argv[1]);
logger.findfile(sys.argv[1]);

#Then we open it
logger.open();

#Let's make a MATLAB variable
import numpy as np
outdata = np.array([0.,0.])
val = 0.999999;

#We create a loop to write stuff
t0 = time.time()
for i in range(0,10):
	print("Time = " + str(time.time()-t0))

	#Populate the outdata Matrix
	outdata[0] = time.time()-t0
	outdata[1] = val
	logger.println(outdata);

	#Change Val
	val = val**2.0

	time.sleep(0.1)
