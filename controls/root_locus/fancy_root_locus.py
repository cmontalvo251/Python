import numpy as np
import matplotlib.pyplot as plt
import control as ctl
import scipy.signal as sci
import sys

##############DEFINE THE PLANT###############
plant_zeros = []
plant_poles = [-3,3]
plant_gain = [1]

##############DEFINE THE CONTROLLER##########

controller_zeros = [-5,-10]
controller_poles = [0]
controller_gain = [1]

##############DEFINE THE SENSOR############

sensor_zeros = []
sensor_poles = []
sensor_gain = [1]

##############DEFINE THE LOCUS##############

KMAX = 100
KSTEP = 1.0
KSTAR = 80.0

######DO NOT EDIT ANYTHING BELOW THIS LINE#######

#Create the Plant Transfer Function
[NG,DG] = sci.zpk2tf(plant_zeros,plant_poles,plant_gain)
G = ctl.tf(NG,DG)
print('G=')
print(G)
#Create the Controller Transfer Function
[NC,DC] = sci.zpk2tf(controller_zeros,controller_poles,controller_gain)
C = ctl.tf(NC,DC)
print('C=')
print(C)
#Create the sensor transfer function
[NH,DH] = sci.zpk2tf(sensor_zeros,sensor_poles,sensor_gain)
H = ctl.tf(NH,DH)
print('H=')
print(H)

##PLOT POLES AND ZEROS OF PLANT AND CONTROLLER
plt.plot(np.real(plant_zeros),np.imag(plant_zeros),'go',label='Plant Open Loop Zeros',markersize=10)
plt.plot(np.real(plant_poles),np.imag(plant_poles),'gx',label='Plant Open Loop Poles',markersize=15)
plt.plot(np.real(controller_zeros),np.imag(controller_zeros),'ro',label='Controller Zeros',markersize=10)
plt.plot(np.real(controller_poles),np.imag(controller_poles),'rx',label='Controller Poles',markersize=15)
plt.plot(np.real(sensor_zeros),np.imag(sensor_zeros),'co',label='Sensor Zeros',markersize=10)
plt.plot(np.real(sensor_poles),np.imag(sensor_poles),'cx',label='Sensor Poles',markersize=15)

##Determine Range on plots
xmins = []
ymins = []
xmaxs = []
ymaxs = []
def addmin(input):
    global xmins,ymins
    if len(input) > 0:
        xmins.append(np.min(np.real(input)))
        ymins.append(np.min(np.imag(input)))
def addmax(input):
    global xmaxs,ymaxs
    if len(input) > 0:
        xmaxs.append(np.max(np.real(input)))
        ymaxs.append(np.max(np.imag(input)))
addmin(plant_poles)
addmin(plant_zeros)
addmin(controller_poles)
addmin(controller_zeros)
addmin(sensor_poles)
addmin(sensor_zeros)
addmax(plant_poles)
addmax(plant_zeros)
addmax(controller_poles)
addmax(controller_zeros)
addmax(sensor_poles)
addmax(sensor_zeros)
xmin = np.min(xmins)
xmax = np.max(xmaxs)
ymin = np.min(ymins)
ymax = np.max(ymaxs)

#Closed Loop TF function
def closed_loop(k,C,G,H):
    return ctl.minreal(k*C*G/(1+k*C*G*H),verbose=False)

##Checking Range Function
def check_range(input):
    global xmin,xmax,ymin,ymax
    if len(input) > 0:
        mp = np.min(np.real(input))
        mxp = np.max(np.real(input))
        if mp < xmin:
            xmin = mp
        if mxp > xmax:
            xmax = mxp
        ymp = np.min(np.imag(input))
        ymxp = np.max(np.imag(input))
        if ymp < ymin:
            ymin = ymp
        if ymxp > ymax:
            ymax = ymxp

###LOOP ON K TO MAKE LOCUS
print('Calculating...')
k_vec = np.arange(KSTEP,KMAX,KSTEP)
#p_vec = []
#z_vec = []
for k in k_vec:
    #Compute closed loop TF
    GCL = closed_loop(k,C,G,H)
    poles = ctl.pole(GCL)
    zeros = ctl.zero(GCL)
    #Check range on plot
    check_range(poles)
    check_range(zeros)
    #Plot poles and zeros
    #p_vec.append(poles)
    #z_vec.append(zeros)
    plt.plot(np.real(poles),np.imag(poles),'b*')
    plt.plot(np.real(zeros),np.imag(zeros),'r*')
plt.plot(np.real(poles),np.imag(poles),'b*',label='Root Locus')
plt.plot(np.real(zeros),np.imag(zeros),'r*',label='Zero Locus')

#This part doesn't quite work yet because
#I think MATLAB uses an adaptive step to compute
#the locuse
#Convert to Numpy Array
#p_vec = np.asarray(p_vec)
#z_vec = np.asarray(z_vec)
#Plot locus
#nrc = np.shape(p_vec)
#Np = nrc[1]
#for i in range(0,Np):
#    plt.plot(np.real(p_vec[:,i]),np.imag(p_vec[:,i]),'b-')

#Now compute the transfer function for KSTAR
GCL = closed_loop(KSTAR,C,G,H)
print('GCL = ')
print(GCL)
star_poles = ctl.pole(GCL)
star_zeros = ctl.zero(GCL)
plt.plot(np.real(star_poles),np.imag(star_poles),'ms',label='K='+str(KSTAR))
tout,yout = ctl.step_response(GCL)

print('Done')

#Last minute range check
if xmax < 0:
    xmax = -0.1*xmin
if ymin == ymax:
    ymin = xmin
    ymax = -ymin
    
xmax *= 1.11
xmin *= 1.11
ymin *= 1.11
ymax *= 1.11
    
#Extra Bits
#Plot real and imaginary axes
plt.plot([xmin,xmax],[0,0],'k-')
plt.plot([0,0],[ymin,ymax],'k-')
#Set Range
plt.xlim([xmin,xmax])
plt.ylim([ymin,ymax])
#Set labels
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.legend()
plt.grid()

plt.figure()
plt.plot(tout,yout)
plt.xlabel('Time (sec)')
plt.ylabel('Y')
plt.title('Step Response (K = '+str(KSTAR)+')')
plt.grid()

plt.show()
