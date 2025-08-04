#!/usr/bin/python

from pdf import *
from pitot_probe import *
import plotting as P
import mio as I
import sys

#0 = PDF and 1 = plots
pp = PDF(0,plt)

if len(sys.argv) > 5:
    root_dir = sys.argv[1]
    rows = int(sys.argv[2])
    cols = int(sys.argv[3])
    dx = np.float(sys.argv[4])
    dy = np.float(sys.argv[5])
else:
    root_dir = 'Data_Files/Downwash_Experiments/11_16_2017/'
    rows = 2
    cols = 2
    print 'Using Root = ',root_dir,' Rows,Cols = (',rows,',',cols,')'


#Need to make our contour plot
WINDS = np.zeros([rows+2,cols+2]) #Pad everything with zeros
r = 0
c = 0
dx = 2.0
dy = 2.0
xvec = np.arange(0,(rows+2)*dx,dx)
yvec = np.arange(0,(cols+2)*dy,dy)

#Need to read in every data stream in the folder
all_pitots = []
for i in range(0,1000):
    hundreds = str(i/100);
    tens = str((i/10)%10);
    ones = str(i%10);
    fileName = 'GPS__'+hundreds+tens+ones+'.TXT'
    try:
        data = I.dlmread(root_dir + fileName,' ',suppressWarnings=True)
    except:
        data = None
    if data != None:
        #Make the pitot class
        print fileName
        pit = Pitot(data[:,0],data[:,1],fileName)
        #First let's run each pitot probe through the convert_pitot routine
        #2 is bit threshold for truncation filter
        #25 is the crossover frequency for lowpass filter from truncated bits to filtered bits
        #0.03 is the sigma filter for the complimentary filter from airspeed to filtered airspeed
        pit.convert_pitot(bit_threshold=2,wc=-99,sigma=0.03)
        #Then let's plot everything but as a place holder let's just plot the raw bits
        pit.plot_processed_bits(pp)
        #Thing is we need one single data point so run
        pit.get_single_data_point()
        #Then put ths in the data ball
        if r == rows: #Check for overflow
            print 'Rows and Columns set incorrectly'
            sys.exit()
        WINDS[r+1][c+1] = pit.WIND
        c+=1
        if c == cols:
            c = 0
            r+=1
        #Finally I want to plot windspeed for all of them
        pit.plot_windspeed(pp)
        #Then concatenate it to a big data ball for later
        all_pitots.append(pit)

#print WINDS
XMAT,YMAT = np.meshgrid(xvec,yvec)
#print XMAT
#print YMAT
#Now let's make the contour plot
plti = P.plottool(12,'X (in)','Y (in)','DownWash (m/s)')
CS = plti.contour(XMAT,YMAT,WINDS)
plti.clabel(CS, inline=1, fontsize=10)
pp.savefig()
#Let's do a mesh as well - or wireframe
axi = P.plotwire(XMAT,YMAT,WINDS,'X (in)','Y (in)','DownWash (m/s)','3DRobotics')
pp.savefig()
#PDF clean up
pp.close()

