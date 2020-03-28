#!/usr/bin/python

##Import modules
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from xfoiltools import computeclcd

### Get ready for straight to pdf
os.system('rm plots.pdf')
pdfhandle = PdfPages('plots.pdf')

aoa_vec = np.linspace(-15,15,10)
cl_vec = 0*aoa_vec
cd_vec = 0*aoa_vec

##############PARAMETERS###########
NACA       = '0012'
numNodes   = '150'
Re         = '1000000'
Mach       = '0.2'
saveFlnmAFp = 'Airfoil'
saveFlnmCpp = 'Cp'
xfoilFlnm  = 'xfoil_input.txt'

for actr in range(0,len(aoa_vec)):

    AoA = str(aoa_vec[actr])

    saveFlnmAF = saveFlnmAFp + AoA + '.txt'
    saveFlnmCp = saveFlnmCpp + AoA + '.txt'

    # Delete files if they exist
    if os.path.exists(saveFlnmAF):
        os.remove(saveFlnmAF)
    if os.path.exists(saveFlnmCp):
        os.remove(saveFlnmCp)
    
    # Write all parameters to xfoil input file name
    fid = open(xfoilFlnm,"w")
    fid.write("naca " + NACA + "\n")
    fid.write("ppar\n")
    fid.write("N " + numNodes + "\n")
    fid.write("\n\n")
    fid.write("psav " + saveFlnmAF + "\n\n")
    fid.write("oper\n")
    fid.write("visc " + Re + "\n") #Turn this on if you want viscous effects
    fid.write("Mach " + Mach + "\n") #Turn this on if you want viscous effects
    fid.write("alfa " + AoA + "\n")
    fid.write("cpwr " + saveFlnmCp + "\n\n")
    fid.write("quit \n")
    fid.close()
    #print('Running Xfoil with following input deck:')
    #os.system('cat xfoil_input.txt')

    ###############Run XFOIL######################
    os.system('xfoil < xfoil_input.txt')

    if actr == 0:
        PLOTAIRFOIL = 1
    else:
        PLOTAIRFOIL = 0
    cl,cd = computeclcd(AoA,saveFlnmAF,saveFlnmCp,pdfhandle,PLOTAIRFOIL)

    cl_vec[actr] = cl
    cd_vec[actr] = cd

plt.figure()
plt.plot(aoa_vec,cl_vec)
plt.xlabel('Angle of Attack (deg)')
plt.ylabel('Lift Coefficient')
plt.grid()
pdfhandle.savefig()

plt.figure()
plt.plot(aoa_vec,cd_vec)
plt.xlabel('Angle of Attack (deg)')
plt.ylabel('Drag Coefficient')
plt.grid()
pdfhandle.savefig()

plt.figure()
plt.plot(cd_vec,cl_vec)
plt.xlabel('Drag Coefficient')
plt.ylabel('Lift Coefficient')
plt.grid()
pdfhandle.savefig()

plt.figure()
plt.plot(aoa_vec,cl_vec/cd_vec)
plt.xlabel('Angle of Attack (deg)')
plt.ylabel('Lift to Drag Ratio')
plt.grid()
pdfhandle.savefig()

###Close pdf populator
pdfhandle.close()
##Open plots
os.system('evince plots.pdf &')
