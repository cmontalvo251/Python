from numpy import *
from matplotlib.pyplot import *
from scipy.integrate import *

close("all")

## J * phidbldot = T1*d - T2*d
## T = kt*w^2
## T1  = kt*w1^2
## T2 = kt*w2^2
## w1 = w0 + dw
## w2 = w0 - dw

#z is the array of states
#z = [phi,phidot]
#zdot = [phidot,phidbldot]

w1 = 0
w2 = 0

def DerivativesNL(z,t):
    global w1,w2
    J = 0.00367319330305115 #slugs/ft^3
    kt = 0.0335291245362469 
    w0 = 800 #rad/s
    d = 0.7283465 #ft
    phi = z[0]
    phidot = z[1]
    #No control
    dw = 0
    #Let's do a step
    dw = 1
    #let's add prop gain
    phi_c = 20
    e = phi-phi_c
    kp = -50
    dw = kp*e
    #Let's add der gain
    phidot_c = 0
    edot = phidot - phidot_c
    kd = -8
    dw = kp*e + kd*edot
    w1 = w0 + dw
    w2 = w0 - dw
    if w1 > 1250.0:
        w1 = 1250.0
    if w2 > 1250.0:
        w2 = 1250.0
    if w1 < 0:
        w1 = 0
    if w2 < 0:
        w2 = 0
    T1  = kt*w1**2
    T2 = kt*w2**2

    phidbldot = T1*d - T2*d
    
    zdot = np.asarray([phidot,phidbldot])
    
    return zdot
    
tout = linspace(0,10,10000)
zinitial = np.asarray([0,0])
zout = odeint(DerivativesNL,zinitial,tout)

#Extract control effort
w1out = 0*tout
w2out = 0*tout
for idx in range(0,len(tout)):
    DerivativesNL(zout[idx,:],tout[idx])
    w1out[idx] = w1
    w2out[idx] = w2

## PHI/DW = 2d/J / s^2
# poles = 0,0
# zeros = N/A
# gain = 2*d/J
# stable? - Barely marginally stable why? on the axis

plot(tout,zout[:,0],label='Angle')
plot(tout,zout[:,1],label='Rate')

grid()
xlabel('Time (sec)')
ylabel('State')
legend()

figure()
plot(tout,w1out)
plot(tout,w2out)

show()