import numpy as np

##INPUTS
RT = 2000.0
Vi = 20.0
Voideal = 5.0
Ro = 1000000000.0
Rs = 120.0

#Calculations
R2 =  Voideal / Vi * RT
print('R2 = ',R2)
R1 = RT - R2
print('R1 = ',R1)
Req = R2 * Ro / (Ro + R2)
print('Req = ',Req)
Vo = Vi * Req /(Rs + R1 + Req)
print('Vo = ',Vo)
eps = (Voideal - Vo)/Voideal * 100
print('Loading Error (%) = ',eps)