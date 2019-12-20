import numpy as np
import matplotlib.pyplot as plt
import control as ctl

##Parameters
g = 9.81
L = 1.0
m = 5.0
#Roots of Zeros
z1 = -10
z2 = -4
#(s + o+wj) * (s + o-wj)
#(s^2 + (o+wj)*s + (o-wj)*s + (o+wj)*(o-wj))
alfa = -(z1+z2)
beta = z1*z2
print(alfa,beta)

def Controller(k):
    global alfa,beta
    N = [k,k*alfa,k*beta]
    D = [1,0]
    C = ctl.tf(N,D)
    zeros = np.roots(N)
    poles = np.roots(D)
    return C,zeros,poles

##DEFINE THE PLANT
G = ctl.tf([1/(m*L**2)],[1,0,-g/L])

##PLOT POLES AND ZEROS OF PLANT AND CONTROLLER
open_poles = ctl.pole(G)
open_zeros = ctl.zero(G)
plt.plot(np.real(open_poles),np.imag(open_poles),'gx',label='Plant Open Loop Poles',markersize=15)
plt.plot(np.real(open_zeros),np.imag(open_zeros),'go',label='Plant Zeros',markersize=10)
C,zeros,poles = Controller(1)
plt.plot(np.real(zeros),np.imag(zeros),'ro',label='Control Zeros',markersize=10)
plt.plot(np.real(poles),np.imag(poles),'rx',label='Control Poles',markersize=15)

###LOOP ON K TO MAKE LOCUS
k_vec = np.linspace(0,1000,1000)
for k in k_vec:
    #print(k)
    C,zeros,poles = Controller(k)
    GCL = C*G/(1+C*G)
    poles = ctl.pole(GCL)
    plt.plot(np.real(poles),np.imag(poles),'b*')
plt.legend()
plt.grid()
plt.show()

