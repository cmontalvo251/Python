###Modules to Import
import numpy as np ##numeric computatio and arrays
import matplotlib.pyplot as plt #plotting
import os #allows me to make calls to my terminal
import time

###Compile Fortran Code
print('Removing a.out')
os.system('rm a.out')
print('Compiling Fortran Code')
os.system('gfortran Parachute.f90 -w')
print('Run Fortran Code')
##Run Fortran Code
os.system('rm ParachuteResults_FORTRAN.txt')
start_time = time.time()
os.system('./a.out > file')
end_time = time.time()
FORTRAN_TIME = end_time - start_time
print('Fortran Time = ',FORTRAN_TIME)

##Import the Fortran Data
fortran_data = np.loadtxt('ParachuteResults_FORTRAN.txt')
print(np.shape(fortran_data))
time_f = fortran_data[:,0]
altitude_f = -fortran_data[:,1]
velocity_f = fortran_data[:,2]

############RUN THE PYTHON VERSION#############

def Derivatives(state):
	m = 80.0 #!mass of skydiver
	g = 9.81 #!gravity     
	rho = 1.28 #!density of air
	A = 0.7 #!Cross-Sectional Area of parachute        	
	cd = 1.0 #!Drag coefficient 
	
	z = state[0]
	zdot = state[1]
	zdbldot = g - (0.5*rho*(zdot**2)*A*cd)/m

	return np.array([zdot,zdbldot])

##Initialize Variables
start_time = time.time()
STATE = np.array([0.,0.])
STATEDOT = np.array([0.,0.])
NEWSTATE = np.array([0.,0.])
n = 50000
t = 0.0
dt = 0.01
##Initial Conditions
STATE[0] = -500.0 #!z
STATE[1] = -30.0  #!zdot 

##Open Outputfile
fid = open('ParachuteResults_Python.txt','w')

##Loop Through Euler Method
i = 1
while STATE[0] < 0 and i < n:

	##Increment counter
	i+=1

	##Output Contents to file
	outstr = str(t) + ' '
	for s in STATE:
		outstr+=str(s)
		outstr+=' '
	for s in STATEDOT:
		outstr+=str(s)
		outstr+=' '
	outstr+='\n'
	#print(outstr)
	fid.write(outstr)

	#print('Simulation ' + str(i/n*100) + ' % Complete')

	STATEDOT = Derivatives(STATE)
	NEWSTATE = STATE + dt*STATEDOT
	STATE = NEWSTATE
	t = t + dt

#Close the file
fid.close()
end_time = time.time()
PYTHON_TIME = end_time - start_time
print('Python Time = ',PYTHON_TIME)

##Import the Fortran Data
python_data = np.loadtxt('ParachuteResults_Python.txt')
print(np.shape(python_data))
time_p = python_data[:,0]
altitude_p = -python_data[:,1]
velocity_p = python_data[:,2]

###############################################

#Plot Everything
plt.figure()
plt.plot(time_f,altitude_f,label='Fortran')
plt.plot(time_p,altitude_p,'--',label='Python')
plt.xlabel('Time (sec)')
plt.ylabel('Altitude (m)')
plt.grid()
plt.legend()

plt.figure()
plt.plot(time_f,velocity_f,label='Fortran')
plt.plot(time_p,velocity_p,'--',label='Python')
plt.xlabel('Time (sec)')
plt.ylabel('Velocity (m/s)')
plt.grid()
plt.legend()

plt.show()




