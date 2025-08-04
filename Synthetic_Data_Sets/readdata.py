#!/usr/bin/python3
import numpy as np

###THIS WILL READ A SYNTHETIC DATA SET
##Open File
file = open('data/0.csv')
ctr = 0
##Create empty array
data = []
for line in file:
	##Split lines by commas
	row = line.split(',')
	##First row is the header info
	if ctr == 0:
		header = row
		print(header)
	else:
		##Convert entire row to numpy floats
		numpyrow = [np.float(i) for i in row]
		data.append(numpyrow)
	ctr+=1

##Convert entire data set to numpy array
data = np.array(data)
r,c = np.shape(data)
print('Size of Data Set (row,columns) = ',r,c)

###EVERYTHING BELOW HERE WILL MAKE A PDF FOR VIEWING PURPOSES
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys
import os
pdfhandle = PdfPages('plots.pdf')
for i in range(0,c):
	plt.figure()
	plt.plot(data[:,i])
	plt.xlabel('Count')
	plt.grid()
	plt.ylabel(header[i])
	print(i,header[i],c)
	pdfhandle.savefig()
pdfhandle.close()
if sys.platform == 'linux2' or sys.platform == 'linux':
	print('Opening Plots')
	os.system('evince plots.pdf &')
#plt.show()