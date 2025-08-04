###This routine will generate the empirical formula for 
##one pitot probe
import numpy as np
import matplotlib.pyplot as plt
import plotting as P #this is in BlackBox.git

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
    
##Close all figures
plt.close("all")

##Let's test our pitot probe equation
v0 = 1.0
psi = np.linspace(-2*np.pi,2*np.pi,1000)
for x in range(0,1):
    vhat = pitot(v0,psi,x)
    plt.plot(psi,vhat,label='Sensor'+str(x))
plt.legend()


##Ok now let's set v0 and psi to a constant
v0 = 2.2;
psi =3.0*np.pi/5.0
##Let's compute our 4 measured signals
v_signals = Get_Pitot(v0,psi)

print 'Four Measured Signals = ',v_signals

##Now let's test our cost function. J should be 0
J0 = J(v_signals,v0,psi)
print 'J0 = ',J0,' <---this should be zero'

##This routine is quick but it's not optimal.
##What we probably need to do is run this routine first. Then use NR
#To finish it off. Or Steepest descent. I don't want to code that though.
#Let's just use four_pitot_optimization.py

##Ok so we know that the minimum is going to be constant across angle
##So let's determine that first
N = 10000
test_angles = np.linspace(-np.pi,np.pi,N)
Jmin = 1e20
for angle in test_angles:
    #Compute cost
    Ja = J(v_signals,2.0,angle) #Just assume you already know v = 1
    if Ja < Jmin:
        Jmin = Ja
        psi_answer = angle
##Now that we have the angle we can find the speed
test_speed = np.linspace(0,10,N)
Jmin = 1e20
for speed in test_speed:
    #COmpute cost
    Js = J(v_signals,speed,psi_answer)
    if Js < Jmin:
        Jmin = Js
        v_answer = speed 
##Print the answer. Did we get the right answer?
print "Actual (m/s, deg) = ",v0,180.0/np.pi*psi
print "Solution (m/s, deg) = ",v_answer,180.0/np.pi*psi_answer
J_answer = J(v_signals,v_answer,psi_answer)
print "Cost Function = ",J_answer
v_empirical = Get_Pitot(v_answer,psi_answer)
print "Signals using Solution = ",v_empirical
print "Percent Error (m/s, deg) = ",100.0*(v_answer-v0)/v0,100.0*(psi_answer-psi)

plt.show()
