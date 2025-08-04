#!/usr/bin/python

import sys
import os
import numpy as np
import getpass
#Import mesonet module
sys.path.append('Mesonet')
import mesonet as MES
#Import pitot module
sys.path.append('FASTPitot/')
import pitot as FP
#Import imet module 
sys.path.append('iMet/')
import iMet as MET
#Import Quad module
#sys.path.append('Quad/')
import quad as Q #This has moved to BlackBox
#Import Anemometer module
sys.path.append('Anemometer/')
import anemometer as ANEM
#Import extra stuff
import gps as GPS
import mymath as M
import math
from pdf import PDF
import plotting as myplot
import matplotlib.pyplot as plt
import sixdof as SDOF

###Cost Function
def J(vtilde,v0,psi):
    J = 0.0
    for x in range(0,4):
        J += (vtilde[x]-pitot(v0,psi,x))**2
    return J
    
###Empirical Formula for Pitot probe
def pitot(v0,psi,i):
    psi_i = psi - (i)*np.pi/2 #Remember that python starts at 0 
    #if psi in between 135 and 225 vhat = 0 else use the formula below
    coeff = np.asarray([0.20343723,0.71429915,0.28590535,-0.24011622])
    c0 = 0.0530172884654
    ##Old data
    #coeff = np.asarray([0.14666216,0.66244758,0.23224845,-0.22226221])
    #c0 = -0.025
    ##Use empirical formula
    vhat = c0
    L = 2.0*np.pi
    N = len(coeff)
    for n in range(N):
        wn = 2.0*np.pi*(n+1)/L
        vhat += coeff[n]*np.cos(wn*psi_i)
    return vhat*v0
    
def Get_Pitot(v,psi):
    vout = []
    for x in range(0,4):
        vout.append(pitot(v0,psi,x))
    return(np.asarray(vout))

#Grab the pitot data
pFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/04_13_2017/FP4V/FP4V.TXT'
numPitots = 4
sigma_pitot = 1.0 #this turns everything off
#wc = 100.0 #this is set in pitot.py 
#truncation_bits = 1.5 #this is set in pitot.py
CAL_TIMES_i = [25,35]
data_pitot = FP.get_pitot_data(pFile,numPitots,sigma_pitot,CAL_TIMES_i)

# pFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/Quad_Square_Pattern/FP4V.TXT'
# numPitots = 4
# sigma_pitot = 1.0 #this turns everything off
# #wc = 100.0 #this is set in pitot.py 
# #truncation_bits = 1.5 #this is set in pitot.py
# CAL_TIMES_i = [5,20]
# data_pitot = FP.get_pitot_data(pFile,numPitots,sigma_pitot,CAL_TIMES_i)

# pFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/Apprentice_Square_Pattern/FP4V_GPSLO103.TXT'
# numPitots = 4
# sigma_pitot = 1.0 #this turns everything off
# #wc = 100.0 #this is set in pitot.py 
# #truncation_bits = 1.5 #this is set in pitot.py
# CAL_TIMES_i = [-99,0]
# data_pitot = FP.get_pitot_data(pFile,numPitots,sigma_pitot,CAL_TIMES_i)

alg_v = []
alg_psi = []
VX = []
VY = []
VZ = []

pitot_signal_1 = data_pitot[1][1][0]
pitot_signal_2 = data_pitot[1][1][1]
pitot_signal_3 = data_pitot[1][1][2]
pitot_signal_4 = data_pitot[1][1][3]

N = 100 #Obviously increasing this gives us a more accurate measurement. But it
#also slows down the code.
v_guess = np.linspace(0,20,N)
psi_guess = np.linspace(-np.pi,np.pi,N)

print 'Running Algorithm'

l = len(pitot_signal_1)

fid = open('Compiled_Data/Lisa_Final_Thesis_Experiments/04_13_2017/Algorithm_Output.txt','w')
#fid = open('Compiled_Data/Lisa_Final_Thesis_Experiments/Quad_Square_Pattern/Algorithm_Output.txt','w')
#fid = open('Compiled_Data/Lisa_Final_Thesis_Experiments/Apprentice_Square_Pattern/Algorithm_Output.txt','w')

for i in range (0,l):
    print 'Running Algorithm = ',i,'out of',l
    #This is horrible. Let's change it
    #v_signals = [data_pitot[1][1][0][i], data_pitot[1][1][1][i], data_pitot[1][1][2][i], data_pitot[1][1][3][i]]
    v_signals = [pitot_signal_1[i],pitot_signal_2[i],pitot_signal_3[i],pitot_signal_4[i]]
    ##Sweet. Alright let's do a double for loop now through v0 and psi
    x = -1
    Jmin = 1e20
    for v in v_guess:
        x += 1
        y = -1
        for p in psi_guess:
            y+=1
            Jvp = J(v_signals,v,p)
            if Jvp < Jmin:
                Jmin = Jvp
                v_answer = np.copy(v)
                psi_answer = np.copy(p)
    #Is this necessary? Yea sure.
    #alg_v.append(v_answer)
    #alg_psi.append(180.0/np.pi*psi_answer) #alg_psi is in degrees

################THEN CONVERT TO VX AND VY###################

    #psi_answer is in radians already
    #VX.append(v_answer*np.cos(psi_answer))
    #VY.append(v_answer*np.sin(psi_answer))

    #Write everything to a text file
    outstring = str(v_answer)+" "+str(180.0/np.pi*psi_answer)+" "+str(v_answer*np.cos(psi_answer))+" "+str(v_answer*np.sin(psi_answer))+"\n"
    fid.write(outstring)

#############################################################
fid.close()

print 'Algorithm Finished'
