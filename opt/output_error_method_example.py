###Output error method
import numpy as np
import matplotlib.pyplot as plt

##Alright our delJ is a FDM
def FDM(sguess,Tperfect,timeperfect):
    ds = 0.01
    costUp = cost(sguess + ds,Tperfect,timeperfect)
    costDown = cost(sguess - ds,Tperfect,timeperfect)
    delJ = (costUp-costDown)/(2*ds)
    return delJ

##Our cost function goes like this
def cost(sguess,Tperfect,timeperfect):
    Tguess = temperature(sguess,timeperfect)
    J = np.sum((Tguess-Tperfect)**2)
    return J

#This function will be used to create our data and for optimization
def temperature(s,time):
    global dt
    T0 = 72.0
    TF = 400.0
    #T = TF + (T0-TF)*np.exp(-s*time)
    #Instead integrate the equations using Euler's Method
    #Tdot = (TF-T)*s
    T = 0*time
    T[0] = T0
    for i in range(0,len(time)-1):
        Tdot = (TF-T[i])*s
        T[i+1] = T[i] + Tdot*dt
    return T

##Let's assume that we have perfect temperature data
dt = 0.01
sperfect = 10.0
timeperfect = np.arange(0,2,dt)
Tperfect = temperature(sperfect,timeperfect)

##My students in ME316 just have to guess
ts = 0.5
tau = ts/4.0
sgraph = 1/tau
Tgraph = temperature(sgraph,timeperfect)

##CURVE FIT has been used - AI - No need. This is overkill really.

##Newton-Raphson with an alfa parameter using the fit
sguess = 20.0
J = cost(sguess,Tperfect,timeperfect)
alfa = 1.0
print('Initial Parameters = ',sguess,J,alfa)
while alfa > 0.01 and J > 1e-8:
    delJ = FDM(sguess,Tperfect,timeperfect)
    snew = sguess - J/delJ*alfa
    Jnew = cost(snew,Tperfect,timeperfect)
    if Jnew < J:
        J = Jnew
        sguess = snew
        print('Computed new guess variable = ',snew,J,alfa)
    else:
        alfa /= 2.0
        print('Reducing alfa.....',alfa)
##Alright now compute our best guess based on the output of the N-R with alfa technique
TNR = temperature(sguess,timeperfect)

##We are trying to estimate s
print('Sperfect = ',sperfect)
print('Sgraph = ',sgraph)
print('S OEM = ',snew)

##Now let's plot our temperature
plt.figure()
plt.grid()
plt.plot(timeperfect,Tperfect,'b-s',label='Perfect Data')
plt.plot(timeperfect,Tgraph,'r--',label='Guess based on graph')
plt.plot(timeperfect,TNR,'k--',label='Output of N-R')
plt.legend()
plt.show()