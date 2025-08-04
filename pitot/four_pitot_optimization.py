###This routine will generate the empirical formula for 
##one pitot probe
import numpy as np
import matplotlib.pyplot as plt
import plotting as P #this is in BlackBox.git
import scipy.interpolate as sci_int
import sys

###Cost Function
def J(vtilde,v0,psi):
    J = 0.0
    for x in range(0,4):
        J += (vtilde[x]-pitot(v0,psi,x))**2
    return J
    
def pitot(v0,psi,i):
    #return pitot_interp(v0,psi,i)
    return pitot_cosine(v0,psi,i)
    
###Empirical Formula for Pitot probe
def pitot_interp(v0,psi,i):
    psi_i = psi - (i)*np.pi/2 #Remember that python starts at 0 
    #if psi in between 135 and 225 vhat = 0 else use the formula below
    if type(psi_i) == type(np.array([1,1])):
        for ctr in range(0,len(psi_i)):
            if psi_i[ctr] < 0:
                psi_i[ctr] += np.pi*2
    else:
        #print psi_i
        if psi_i < 0:
            psi_i += np.pi*2
    psi_interp = np.asarray([0.,45.,90.,135.,180.,225.,270.,315.,360.])*np.pi/180.0
    vhat_interp = np.asarray([0.95632245,0.11437906,-1.02183877,0.23100659,-0.08258305,0.23100659,-1.02183877,0.11437906,0.95632245])
    vhat = np.interp(psi_i,psi_interp,vhat_interp)
    #print vhat
    return vhat*v0
    
###Empirical Formula for Pitot probe
def pitot_cosine(v0,psi,i):
    psi_i = psi - (i)*np.pi/2 #Remember that python starts at 0 
    #if psi in between 135 and 225 vhat = 0 else use the formula below
    if type(psi_i) == type(np.array([1,1])):
        for ctr in range(0,len(psi_i)):
            if psi_i[ctr] < 0:
                psi_i[ctr] += np.pi*2
    else:
        #print psi_i
        if psi_i < 0:
            psi_i += np.pi*2
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
    #print vhat
    return vhat*v0
    
def Get_Pitot(v,psi):
    vout = []
    for x in range(0,4):
        vout.append(pitot(v0,psi,x))
    return(np.asarray(vout))
    
##Close all figures
plt.close("all")

##Let's test our pitot probe equation
v0 = 1.0
psi = np.linspace(-2*np.pi,2*np.pi,1000)
for x in range(0,1):
    vhat = pitot(v0,psi,x)
    plt.plot(psi*180.0/np.pi,vhat,label='Sensor'+str(x))
plt.xlabel('Angle (deg)')
plt.ylabel('Magnitude Factor (nd)')
plt.grid()
plt.legend()


##Ok now let's set v0 and psi to a constant
v0 = 3.0;
psi = 45.0*np.pi/180.0
##Let's compute our 4 measured signals
v_signals = Get_Pitot(v0,psi)
print v_signals

sys.exit()
#Matt put your signals here and try one point at a time.
#v_signals = [-4.79044576,5.69981486,-5.21963507,0.39424582]

print 'Four Measured Signals = ',v_signals

##Now let's test our cost function. J should be 0
J0 = J(v_signals,v0,psi)
print 'J0 = ',J0,' <---this should be zero'

##Sweet. Alright let's do a double for loop now through v0 and psi
N = 200 #Obviously increasing this gives us a more accurate measurement. But it
#also slows down the code.
v_guess = np.linspace(0,10,N)
psi_guess = np.linspace(-np.pi,np.pi,N)
if N < 100:
    JJ = np.zeros([N,N])
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
        if N < 100:
            JJ[y][x] = Jvp

if N < 100:        
    VMAT,PSIMAT = np.meshgrid(v_guess,psi_guess*180.0/np.pi)
    #I already have a module for mesh plots in plotting.py
    axi = P.plotwire(VMAT,PSIMAT,JJ,'Wind Speed (m/s)','Direction (deg)','Cost Function','Pitot Optimization')

##Print the answer. Did we get the right answer?
print "Actual (m/s, deg) = ",v0,180.0/np.pi*psi
print "Solution (m/s, deg) = ",v_answer,180.0/np.pi*psi_answer
J_answer = J(v_signals,v_answer,psi_answer)
print "Cost Function = ",J_answer
v_empirical = Get_Pitot(v_answer,psi_answer)
print "Signals using Solution = ",v_empirical
print "Percent Error = ",100.0*abs(v_answer-v0)/v0,100.0*abs(psi_answer-psi)/psi

plt.show()
