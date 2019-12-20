#!/usr/bin/python

import numpy as np 
import matplotlib.pyplot as plt
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages
#from matplotlib.ticker import FormatStrFormatter

uint = 0.0

##Let's make a class to utilize object oriented programming
class Vehicle():
    def __init__(self):
        #Set up Simdata
        T0 = 0.0
        TFINAL = 50
        TIMESTEP = 0.01
        self.simdata = np.asarray([T0,TFINAL,TIMESTEP])
        ##Set up the massdata
        self.mass = 5.6
        Ixx = 1.0
        Iyy = 2.0
        Izz = 3.0
        self.I = np.asarray([[Ixx,0,0],[0,Iyy,0],[0,0,Izz]])
        self.Iinv = np.linalg.inv(self.I)
        ##Set up initial conditions
        x0 = 0.0
        y0 = 0.0
        z0 = -100.0
        phi0 = 30*np.pi/180.
        theta0 = 0.0
        psi0 = 0.0
        u0 = 20.0
        v0 = 0.0
        w0 = 0.0
        p0 = 0.0
        q0 = 0.0
        r0 = 0.0
        self.stateinitial = np.asarray([x0,y0,z0,phi0,theta0,psi0,u0,v0,w0,p0,q0,r0])
        
    def ForceMoment(self,t,state,xyzdot):
        global uint
        z = state[2]
        zdot = xyzdot[2]
        phi = state[3]
        theta = state[4]
        psi = state[5]
        u = state[6]
        v = state[7]
        w = state[8]
        p = state[9]
        q = state[10]
        r = state[11]
        grav=9.81 #Coefficient of Gravity: kg-m/s^2
        cbar=0.2286 #Aerodynamic chord length: m
        bws=1.4859 #Wing span: m
        S=cbar*bws #Cross-sectional area of wings: m^2
        Roe=1.225 #Density of air: kg/m^3
        CLzero = 0.3441029736813229
        CLalpha = 5.185317204810547
        CLq = 5.9369349224934975
        CLdele = 0.41181051485504044
        CDzero = 0.01727851900786801
        CDalpha = 1.0080305157535787
        Cybeta = -0.24095762862664397
        Cydelr = 0.0688450367504697
        Cyp = -0.027733042384004744
        Cyr = 0.17663419386614151
        CLbeta = -0.01633611041536569
        CLp = -0.6583142767075709
        CLr = 0.09800094300447591
        CLdela = -0.19085572159332118
        CLdelr = 0.004667460118675911
        Cmzero = -0.03632475219322319
        Cmalpha= -2.5363576941792045
        Cmq = -17.11816235985625
        Cmdele = -1.0238066966535029
        Cnp = -0.03284800659907888
        Cnbeta = 0.08831709693307076
        Cnr = -0.06906055250375191
        Cndela = 0.216
        Cndelr = -0.17115641081019545
        vinf=np.sqrt(u**2+v**2+w**2) #Stream line velocity: Total velocity
        beta=np.arcsin(v/vinf) #Equation 21: Sideslip angle beta
        alpha=np.arctan(w/u) #Equation 20: Angle of attack alpha
        phat=(p*bws)/(2*vinf)
        qhat=(q*cbar)/(2*vinf)
        rhat=(r*bws)/(2*vinf)
        #CL=CLzero+(CLalpha*alpha)+(CLq*qhat)+(CLdele*dele) #Equation 19: Coefficient of Lift
        #CD=CDzero+(CDalpha*(alpha**2)) #Equation 19: Coefficient of Drag
        #Total Aerodynamic Forces and Thrust:
        W = 12.1 #N
        Uc = 20 #m/s
        Kpt = 75 #Guess

        zc = -100.0
        ThetaC = 0.5*(z-zc) + 0.2*zdot ##outer loop control on altitude
        if ThetaC > 30*np.pi/180.:
            ThetaC = 30*np.pi/180.
        elif ThetaC < -30*np.pi/180.:
            ThetaC = -30*np.pi/180.
        Tmax = 1.2*W #N
        Kt = Tmax/(800**2)
        
        PhiC = 0 #I want wings level
        
        uerror = (Uc-u)
        uint += (0.01/4.0)*uerror
        mewt = Kpt*uerror+1100 + uint

        if mewt < 1100:
           mewt = 1100
        if mewt > 1900:
           mewt = 1900
        T = Kt*(mewt-1100)**2

        Kpe = -1 #Guess and check
        Kde = -.5 #Guess and check

        Kpa = -1 #Guess and check
        Kdp = -0.5 #Guess and check

        Kv = 2.0 #Guess and check
        
        dele = Kpe*(ThetaC-theta)-Kde*q
        dela = Kpa*(PhiC-phi)-Kdp*p
        delr = Kv*r
        
        if dele > 30*np.pi/180.0:
            dele = 30*np.pi/180.0
        elif dele < -30*np.pi/180.0:
            dele = -30*np.pi/180.0
        if dela > 30*np.pi/180.0:
            dela = 30*np.pi/180.0
        elif dela < -30*np.pi/180.0:
            dela = -30*np.pi/180.0
        if delr > 30*np.pi/180.0:
            delr = 30*np.pi/180.0
        elif delr < -30*np.pi/180.0:
            delr = -30*np.pi/180.0
        CL=CLzero+(CLalpha*alpha)+(CLq*qhat)+(CLdele*dele) #Equation 19: Coefficient of Lift
        CD=CDzero+(CDalpha*(alpha**2)) #Equation 19: Coefficient of Drag
        force_weight=self.mass*grav*np.asarray([-np.sin(theta),np.sin(phi)*np.cos(theta),np.cos(phi)*np.cos(theta)])#Equation 17: Weight
        force_aero=0.5*Roe*(vinf**2)*S*np.asarray([(CL*np.sin(alpha))-(CD*np.cos(alpha)),(Cybeta*beta)+(Cydelr*delr)+(Cyp*phat)+(Cyr*rhat),(-CL*np.cos(alpha))-(CD*np.sin(alpha))]) #Equation 18: Aerodynamic forces
        F=force_weight+force_aero+np.asarray([T,0,0])
        #Total Aerodynamic Moments:
        Cm = (Cmzero)+(Cmalpha*alpha)+(Cmq*qhat)+(Cmdele*dele)
        Cl = (CLbeta*beta)+(CLp*phat)+(CLr*rhat)+(CLdela*dela)+(CLdelr*delr)
        Cn = (Cnp*phat)+(Cnbeta*beta)+(Cnr*rhat)+(Cndela*dela)+(Cndelr*delr)
        M=0.5*Roe*(vinf**2)*S*np.asarray([b*Cl,cbar*Cm,b*Cn]) #Equation 23: Aerodynamic moments
        return F,M,np.asarray([mewt,dele,dela,delr,T])
        
    def Derivatives(self,t,state):
        #Need to compute statedot
        #x = state[0]
        #y = state[1]
        #z = state[2]
        phi = state[3]
        theta = state[4]
        psi = state[5]
        u = state[6]
        v = state[7]
        w = state[8]
        p = state[9]
        q = state[10]
        r = state[11]

        #Set up vectors
        ptp = np.asarray([phi,theta,psi])
        uvw = np.asarray([u,v,w])
        pqr = np.asarray([p,q,r])
        
        #Kinematics
        ctheta = np.cos(theta)
        cpsi = np.cos(psi)
        sphi = np.sin(phi)
        stheta = np.sin(theta)
        cphi = np.cos(phi)
        spsi = np.sin(psi)
        ttheta = np.tan(theta)
        TIB = np.asarray([[ctheta*cpsi,sphi*stheta*cpsi-cphi*spsi,cphi*stheta*cpsi+sphi*spsi],[ctheta*spsi,sphi*stheta*spsi+cphi*cpsi,cphi*stheta*spsi-sphi*cpsi],[-stheta,sphi*ctheta,cphi*ctheta]])
        xyzdot = np.matmul(TIB,uvw)
        H = np.asarray([[1.0,sphi*ttheta,cphi*ttheta],[0.0,cphi,-sphi],[0.0,sphi/ctheta,cphi/ctheta]])
        ptpdot = np.matmul(H,pqr)
        
        #Force and Moment Model - These are body frame now
        F,M,control_vars = self.ForceMoment(t,state,xyzdot)
        
        #Dynamics
        uvwdot = F/self.mass - np.cross(pqr,uvw)
        pqrdot = np.matmul(self.Iinv,M-np.cross(pqr,np.matmul(self.I,pqr)))

        dxdt = np.concatenate([xyzdot,ptpdot,uvwdot,pqrdot])

        return dxdt,control_vars

    def Integrate(self):
        #In order to run the RK4 engine we need the simdata block
        #to create a time vector from the simdata block
        tinitial = self.simdata[0]
        tfinal = self.simdata[1]
        timestep = self.simdata[2]
        #Then we can run the RK4 engine
        t = tinitial

        #Although scripting languages like python can plot natively. I will generate an outputfile so if anyone wants
        #to plot in a different language they can.
        outfile = open('Python.OUT','w')

        #Run the integrator
        print('Begin RK4 Integrator')
        state = self.stateinitial
        ctl = np.asarray([0,0,0,0,0])
        while t <= tfinal:
            #Output Contents to File
            liststate = state.tolist()
            s = ", ".join(map(str,liststate))
            listctl = ctl.tolist()
            c = ", ".join(map(str,listctl))
            outfile.write(str(t)+','+s+','+c+'\n')
            #RK4 Call
            k1,ctl1 = self.Derivatives(t,state)
            k2,ctl2 = self.Derivatives(t+timestep/2.0,state+k1*timestep/2.0)
            k3,ctl3 = self.Derivatives(t+timestep/2.0,state+k2*timestep/2.0)
            k4,ctl4 = self.Derivatives(t+timestep,state+k3*timestep)
            phi = (1.0/6.0)*(k1 + 2*k2 + 2*k3 + k4)
            #Step State
            state += phi*timestep
            #print ctl1
            ctl = (1.0/6.0)*(ctl1 + 2*ctl2 + 2*ctl3 + ctl4)
            t+=timestep
            print('Time =',t)
        outfile.close()
        print('RK4 Integration Complete')

if __name__ == '__main__':

    #Create a Vehicle class which also sets all the standard parameters
    mav = Vehicle()

    #Here we go ahead and integrate the equations of motion
    mav.Integrate()

    print('Python Module Complete')

    #Once the integration is complete. It's time to read the entire file and plot all states
    #Although it's possible to simply create vectors like in MATLAB I elected to do it this way
    #to emulate how it would be done in C++ or Fortran.
    file = open('Python.OUT','r')
    data = []
    for line in file:
        row = line.split(',')
        row_np = []
        for r in row:
            row_np.append(np.float(r))
        data.append(row_np)

    data_np = np.asarray(data)
    time = data_np[:,0]
    size = np.shape(data_np)
    NOSTATES = size[1]

    #sys.exit()

    ##Save Figures natively to PDF
    print('Generating Plots')

    pdfhandle = PdfPages('python_plots.pdf')
    ylabels = ['Time (sec)','X (m)','Y (m)','Z (m)','PHI (rad)','THETA (rad)','PSI (rad)','U (m/s)','V (m/s)','W (m/s)','P (rad/s)','Q (rad/s)','R (rad/s)','ESC PWM (us)','Elevator Command (rad)','Aileron Command (rad)','Rudder Command (rad)','Thrust (N)']
    for idx in range(0,NOSTATES):
        plt.figure()
        #print(time)
        #print(data_np[:,idx])
        plt.plot(time,data_np[:,idx])
        plt.grid()
        plt.xlabel('Time (sec)')
        plt.ylabel(ylabels[idx])
        pdfhandle.savefig()
        print(ylabels[idx])
    
    pdfhandle.close()
    print('Plotting Routine Complete for Python')
    os.system('evince python_plots.pdf &')
    #plt.show()

# Copyright - Carlos Montalvo 2016
# You may freely distribute this file but please keep my name in here
# as the original owner
