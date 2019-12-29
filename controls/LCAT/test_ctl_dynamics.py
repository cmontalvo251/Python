import controlsystemdynamics as ctldyn
import numpy as np

###Create state space system matrices
g = 9.81
L = 1.0

#Inverted Pendulum
#A = [[0,1],[-g/L,0]]
#B = [[0],[1]]
#C = [1,0]
#D = [0]

#Segway
m = 40.0
M = 70.0
mbar = m+M
A = [[0,1,0,0],[g*mbar/(M*L),0,0,0],[0,0,0,1],[g*mbar/M-g,0,-0.00001,0]]
B = [[0],[1/(M*L)],[0],[1/M]]
C = [1,0,0,0]
D = [0]

#Create a class instance to analyze everything
sys = ctldyn.makeSystem(A,B,C,D,systype='SS')

#I want this code to work even with the transfer function toolbox
#num = np.asarray([1])
#den = np.asarray([1,0,g/L])
#sys = ctldyn.makeSystem(num,den,systype='TF')

##Integrate openloop no initial conditions
#sys.integrateOpenLoop(0,10,ic=np.asarray([0,0]),input='step')

#Now let's tune the controller
#Since our system is a 2x2 we need to pick one zero and then give parameters for K
sys.rltools(10000,100,5000,[-10,-8],[0]) #KMAX,KSTEP,KSTAR,zeros,poles

#Now is when the magic starts. So now what I want is for the computer to compute K for me
#to put the poles exactly where I want them.
#if sys.place([-10,-11,-2,-3]):
#    print('It worked')
    #With the system poles placed let's plot a root locus
    #sys.rltools(2*sys.KSTAR,1,sys.KSTAR,sys.controller_zeros)

##Integrate the closed loop system
#tfinal = sys.howlong(sys.closedloop_poles)
sys.integrateClosedLoop(0,10,ic=np.asarray([30*np.pi/180,0,0,0]),input='none')
