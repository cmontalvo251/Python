import numpy as np
import matplotlib.pyplot as plt
import control as ctl
import scipy.signal as S

plt.close("all")

#plt.pause(3)


##Proportional Gain
kp_vec = np.linspace(0.5,10,100)

plt.figure()

for kp in kp_vec:
    ###Control Block
    C = kp

    ##Actuator Block
    a = 3.
    A = ctl.tf(a,[1,a])
    
    ###Plant Dynamics
    G = ctl.tf(3,[1,3,2])
    #print(np.roots([1,3,2]))
    
    #print C,A,G
    
    
    ###Open Loop Stuff
    tout = np.linspace(0,8,1000)
    #tout,yout = ctl.step_response(G,tout)
    #plt.plot(tout,yout,label='No Actuator')
    
    #tout,youtA = ctl.step_response(A*G,tout)
    #plt.plot(tout,youtA,label='W Actuator')
    
    #plt.grid()
    #plt.legend()
    
    
    ###Closed Loop Stuff
    #GCL = C*G/(1+C*G)
    #print(GCL)
    GCLA = C*A*G/(1+C*A*G)
    #print(GCLA)
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