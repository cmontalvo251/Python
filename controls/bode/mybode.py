##MAke my own bode
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl
import control.matlab as ctlmtl
import scipy.signal as sci
import sys
#sys.path.append('D:\mtsim\Documents\GitLab_Projects\Multiple_Cube_Sats\Code\MultiSim\BlackBox\pdf')
from pdf import *

###Create A transfer function
#system = ctl.tf([10],[1,2,10])
#print(system)

###Function to get magnitude of TF
def vectormagnitude(vector,s):
    vm = 0
    L = len(vector)
    for v in vector:
        #print(v)
        #print(s)
        vm += v*s**(L-1)
        L -= 1.0
    return vm
    
def getmagnitude(n,d,o):
    G1 = vectormagnitude(n,o*1j)/vectormagnitude(d,o*1j)
    G2 = vectormagnitude(n,-o*1j)/vectormagnitude(d,-o*1j)
    m = np.real(np.sqrt(G1*G2))
    return m

##Given a transfer function make a gain and phase plot
den = [1.00000000, 0.15451050, 0.00445363, 0.00000111, 0.00000003]
num = [0.00000227, 0.00000022, 0.00000001]
system = ctl.tf(num,den)
print(system)
#num,den = ctlmtl.tfdata(system)
#num = num[0][0]
#den  = den[0][0]

omega = np.linspace(10**-7,10**1,100000)
mag = 0*omega
ctr = 0
for o in omega:
    m = getmagnitude(num,den,o)
    mag[ctr] = m
    ctr+=1
    
plt.plot(np.log10(omega),20*np.log10(mag))
plt.grid()
plt.show()