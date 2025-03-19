import numpy as np

###CHAPTER 10

##PROBLEM 5
#Givens
D1 = 10/100 #10 cm
D2 = 7.5/100 #7.5 cm
dP = 10*1000 #10 kPA
Pinf = 700*1000 #1000 kPA
Tinf = 25 #Celsius
#Constants
R = 287. #For air
#Compute Area of Pipes
A1 = (np.pi)*(D1/2)**2
A2 = (np.pi)*(D2/2)**2
#convert celsius to Kelvin
Tk = Tinf + 273.1
#Ideal gas law to compute density
rho = Pinf/(R*Tk)
print('Density of Fluid = ',rho,'kg/m^3')
#Compute flow speed
V2 = 1/np.sqrt(1-(A2/A1)**2)*np.sqrt(2*dP/rho)
print('V2 Flow Rate = ',V2,'m/s')
#Compute volumetric flow rate
Q = V2*A2*60 # *60 for minutes
print('Q Volumetric Flow Rate = ',Q,'m^3/min')
##Mass Flow Rate
mdot = Q*rho
print('Mass Flow Rate = ',mdot,'kg/min')


#Problem 10
#Givens
U = 10.0 #m/s
rho = 1.1 #kg/m^3
dP = (U**2)*rho/2
print('dP = ',dP,' Pa')