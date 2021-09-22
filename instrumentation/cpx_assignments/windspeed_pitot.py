import numpy as np
import matplotlib.pyplot as plt
def voltage(D):
    bits = 2**10
    Vrange = 5.
    return D*Vrange/bits

def pressure(V,Vbias):
    return (V-Vbias)/101.325

def windspeed_compressible(Patm):
    q = (Patm+1)**(2./7.)-1
    k = 5*q
    a0 = 331.
    return a0*np.sqrt(k)

def windspeed_incompressible(Patm):
    Ppascals = 101325*Patm
    rho = 1.225
    return np.sqrt(2*Ppascals/rho)

def brute_force(Patm):
    q = 101325.
    rho = 1.225
    a0 = 331.
    alfa = 2.0*q/(6.05*rho*a0**2)
    return (Patm+1)**(2./7.)-alfa*Patm - 1

Dbias = 520.
Vbias = voltage(Dbias)
Ds = [521,522]
for D in Ds:
    V = voltage(D)
    print(V)
    P = pressure(V,Vbias)
    print(P)
    U = windspeed_compressible(P)
    print(U)

Patm = np.linspace(0.00001,0.5,10000)
plt.figure()
Uc = windspeed_compressible(Patm)
Ui = windspeed_incompressible(Patm)
plt.plot(Patm,Uc,label='Compressible')
plt.plot(Patm,Ui,label='Incompressible')
plt.legend()

plt.figure()
plt.plot(Patm,(Ui-Uc)/Uc-0.1)
plt.plot(Patm,Ui-Uc-0.1*Uc)
plt.plot(Patm,Ui-1.1*Uc)
plt.plot(Patm,Ui**2-1.21*Uc**2)

plt.figure()
plt.plot(Patm,brute_force(Patm))
plt.grid()

Patmc = 0.4396
print(windspeed_compressible(Patmc))

plt.show()