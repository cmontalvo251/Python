#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 07:22:57 2020

@author: carlos
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I

###Closes all Figures
plt.close("all")

def atmosphere_model(altitude):
    global altx,deny
    return np.interp(altitude,altx,deny)    

def planet_parameters():
    ##https://wiki.kerbalspaceprogram.com/wiki/Kerbin
    ##A few things you can compute to compare to the wiki above
    #mu 
    #surface gravity
    #rotational velocity
    
    G = 6.6742*10**-11; #%%Gravitational constant
    Mkerbin = 5.2915158*10**22 #
    muKerbin = -G*Mkerbin
    Rkerbin = 600000 #meters
    sidereal_period = 21549.425
    sidereal_angular_velocity = 2*np.pi/sidereal_period
    sidereal_rotational_velocity = sidereal_angular_velocity*Rkerbin
    surface_gravity = muKerbin*Rkerbin/Rkerbin**3
    return sidereal_rotational_velocity,muKerbin,surface_gravity,Rkerbin
   

#######THIS IS A FUNCTION CALLED A DEFINITION IN PYTHON
#z and t are input. so x = [z,V], x is a 2x1 array with position
# and velocity in it and t is just time.
# matrices are NxM arrays and vectors are Nx1 arrays. Arrays are
# just a way for the computer to handle multiple numbers in one variable
def Derivatives(state,t):

    x = state[0]
    z = state[1]
    velx = state[2]
    velz = state[3]
    mass = state[4]
    
    ###Kinematics
    xdot = velx
    zdot = velz
    
    ##Dynamics
    ## F = m*a
    
    #now let's compute Forces on rocket
    
    ##Gravitational Acceleration
    rSat = np.sqrt((x**2) +(z**2))
    #MNeed to get parameters of the planet
    sidereal_rotational_velocity,mu,surface_gravity,R = planet_parameters()
    gravx = mu*x/(rSat**3)
    gravz = mu*z/(rSat**3)
   
    ##Now let's do Aerodynamics 
    #https://wiki.kerbalspaceprogram.com/wiki/Atmosphere
    #https://wiki.kerbalspaceprogram.com/wiki/Kerbin#Atmosphere
    altitude = rSat-R
    rho = atmosphere_model(altitude)
    #Need AeroGUI Mod to get these parameters
    #https://forum.kerbalspaceprogram.com/index.php?/topic/105524-105-aerogui-v30-14-nov/
    #https://www.youtube.com/watch?v=ASHRPo4sw80
    #A few problems here. First Cd is a function of Mach Number and Reynolds number
    #so......I think I'll just leave this off
    Cd = 0.24
    S = 0.01
    qinf = -np.pi*rho*S*Cd/mass
    aerox = qinf*abs(velx)*velx
    aeroz = qinf*abs(velz)*velz
    
    #And of course thrust
    mass_endtons = 1.4
    mass_end = mass_endtons*2000/2.2
    if mass < mass_end:
        thrustx = 0.0
        thrustz = 0.0
    else:
        thrustx = 81.45*1000.0
        thrustz = 0.0
    thrust = np.sqrt(thrustx**2 + thrustz**2)
    
    #But when thrust is fired we lose mass
    Isp = 140.0
    ve = Isp*abs(surface_gravity)
    mdot = -thrust/ve
    
    ##Now we can put Newton's EOMs together
    xdbldot = thrustx/mass + gravx + aerox
    zdbldot = thrustz/mass + gravz + aeroz
    
    statedot = np.asarray([xdot,zdot,xdbldot,zdbldot,mdot])    
    
    #make [xdot,xdbldot] an array
    return statedot

##############END OF FUNCTION SEPARATED BY TABS#######
    
#Read in Atmospher model
atm_model = np.loadtxt('kerbin_atmosphere.txt')
altx = atm_model[:,0]
deny = atm_model[:,3]

tout = np.linspace(0,100,10000)  #linspace(start,end,number of data points)

sidereal_rotational_velocity,mu,surface_gravity,R = planet_parameters()
x0 = R
z0 = 0.
velx0 = 0.0
velz0 = 0.0
masstons = 2.4
mass0 = masstons*2000/2.2
stateinitial = np.asarray([x0,z0,velx0,velz0,mass0])
stateout = I.odeint(Derivatives,stateinitial,tout) ##This is the ode toolbox from scipy (Scientific Python)

xout = stateout[:,0]
zout = stateout[:,1]
mout = stateout[:,4]

plt.figure()
plt.plot(xout,zout)
plt.grid()
plt.xlabel('X (m)')
plt.ylabel('Z (m)')

plt.figure()
plt.plot(tout,zout)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Z (m)')

plt.figure()
plt.plot(tout,xout-R)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('X (m)')

plt.figure()
plt.plot(tout,mout)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Mass (kg)')

plt.show()

