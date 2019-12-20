import numpy as np
import matplotlib.pyplot as plt
import control as ctl
import scipy.signal as S

plt.close("all")

#plt.pause(3)


##Proportional Gain
kp = 16.
kd = 4.
ki_vec = np.linspace(0,300,100)

plt.figure()

plt.ylim([-12,12])
plt.xlim([-20,5])

for ki in ki_vec:
    ###Control Block
    #C = kp
    
    ###Plant Dynamics
    #G = ctl.tf(4,[1,0,0])
    
    ###Open Loop Stuff
    tout = np.linspace(0,8,1000)
    #tout,yout = ctl.step_response(G,tout)
    #plt.plot(tout,yout,label='No Actuator')
        
    #plt.grid()
    #plt.legend()
        
    ###Closed Loop Stuff
    #GCL = C*G/(1+C*G)
    #print(GCL)
    GCLA = ctl.tf([4*kd,4*kp,4*ki],[1,4*kd,4*kp,4*ki])
    print(GCLA)
    #print(kp)
    
    roots = ctl.pole(GCLA)
    
    print roots
    
    plt.plot(np.real(roots),np.imag(roots),'bs')
    
    #tout,youtCL = ctl.step_response(GCL,tout)
    #tout,youtCLA = ctl.step_response(GCLA,tout)
    
    #plt.plot(tout,youtCL,label='No Actuator')
    #plt.plot(tout,youtCLA,label='W Actuator')
    
    plt.pause(0.1)

    plt.grid()
#plt.legend()
    
plt.show()