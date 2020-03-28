#!/usr/bin/python

##Import modules
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

### Get ready for straight to pdf
os.system('rm plots.pdf')
pdfhandle = PdfPages('plots.pdf')

PLOTAIRFOIL = 1

aoa_vec = np.linspace(-20,20,20)
cl_vec = 0*aoa_vec
cd_vec = 0*aoa_vec

for actr in range(0,len(aoa_vec)):

    AoA = str(aoa_vec[actr])

    ##############PARAMETERS###########
    NACA       = '0012'
    numNodes   = '200'
    Re         = '1000000'
    Mach       = '0.2'
    saveFlnmAF = 'Save_Airfoil.txt'
    saveFlnmCp = 'Save_Cp.txt'
    xfoilFlnm  = 'xfoil_input.txt'

    # CL = 0.3623f
    # CD = -0.00106
    # CM = -0.0042

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
    print('Running Xfoil with following input deck:')
    os.system('cat xfoil_input.txt')

    ###############Run XFOIL######################
    os.system('xfoil < xfoil_input.txt')

    # %% READ DATA FILE: AIRFOIL
    dataBuffer = np.loadtxt(saveFlnmAF, skiprows=0)

    # Extract data from the loaded dataBuffer array
    XB = dataBuffer[:,0]
    YB = dataBuffer[:,1]
    
    # %% READ DATA FILE: PRESSURE COEFFICIENT
    dataBuffer = np.loadtxt(saveFlnmCp, skiprows=1)
    # Extract data from the loaded dataBuffer array
    X_0  = dataBuffer[:,0]
    Cp_0 = dataBuffer[:,1]

    # %% EXTRACT UPPER AND LOWER AIRFOIL DATA
    # Split airfoil into (U)pper and (L)ower
    XB_U = XB[YB >= 0]
    XB_L = XB[YB < 0]
    YB_U = YB[YB >= 0]
    YB_L = YB[YB < 0]
    # Split XFoil results into (U)pper and (L)ower
    Cp_U = Cp_0[YB >= 0]
    Cp_L = Cp_0[YB < 0]
    X_U  = X_0[YB >= 0]
    X_L  = X_0[YB < 0]

    ##The upper surface is backwards which messes with lift calcs
    XB_U = XB_U[-1::-1]
    YB_U = YB_U[-1::-1]
    Cp_U = Cp_U[-1::-1]
    X_U = X_U[-1::-1]

    # %% PLOT DATA
    # Plot airfoil
    if PLOTAIRFOIL == 1:
        plt.figure()
        plt.plot(XB_U,YB_U,'b.-',label='Upper')
        plt.plot(XB_L,YB_L,'r.-',label='Lower')
        plt.xlabel('X-Coordinate')
        plt.ylabel('Y-Coordinate')
        plt.title('Airfoil')
        plt.axis('equal')
        plt.grid()
        plt.legend()
        pdfhandle.savefig()
        PLOTAIRFOIL = 0 

    # Plot pressure coefficient
    plt.figure()
    plt.plot(X_U,Cp_U,'b.-',label='Upper')
    plt.plot(X_L,Cp_L,'r.-',label='Lower')
    plt.xlim(0,1)
    plt.xlabel('X-Axis')
    plt.ylabel('Y-Axis')
    plt.title('Pressure Coefficient = ' + AoA + ' deg')
    plt.legend()
    plt.grid()
    plt.gca().invert_yaxis()
    pdfhandle.savefig()

    # plt.figure()
    # plt.plot(XB_U)
    # plt.plot(XB_L)
    # pdfhandle.savefig()

    ##Compute Lift
    cn = 0
    ca = 0
    for ctr in range(0,len(XB_L)-1):
        print(XB_L[ctr])
        delX = XB_L[ctr+1]-XB_L[ctr]
        cn+=(Cp_L[ctr]-Cp_U[ctr])*delX
        delYu = YB_U[ctr+1]-YB_U[ctr]
        delYl = YB_L[ctr+1]-YB_L[ctr]
        dyudx = delYu/delX
        dyldx = delYl/delX
        ca+=(Cp_U[ctr]*dyudx - Cp_L[ctr]*dyldx)*delX
        print('Normal Coefficient = ',cn)
        print('Axial Coefficient = ',ca)
        alfa = np.float(AoA)*np.pi/180.0
        cl = cn * np.cos(alfa) - ca * np.sin(alfa)
        cd = cn * np.sin(alfa) + ca * np.cos(alfa)
        print('Lift Coefficient = ',cl)
        print('Drag Coefficient = ',cd)
        # Xfoil AoA = 3
        # CL = 0.3623
        # CD = -0.00106
        # CM = -0.0042

        # Xfoil AoA = 10
        # CL = 1.202
        # CD = -0.00120
        # CM = -0.0042

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
