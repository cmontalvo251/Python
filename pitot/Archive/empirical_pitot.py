###This routine will generate the empirical formula for 
##one pitot probe
import numpy as np
import matplotlib.pyplot as plt
import mio as IO
import sys

##Shift by a certain amount
def shift(invec,s):
    outvec = np.concatenate((invec[s:],invec[0:s]))
    return outvec

plt.close("all")

#####ANALYTIC SOLUTION USING 4 COSINE WAVES###############
#Solve for coefficients
#MAT = np.asarray([[1,1,1,1],[0,-1,0,1],[-1,1,-1,1],[-1,0,3,0]])
#sol = np.asarray([1,-1,0,0])
#ABCD = np.matmul(np.linalg.inv(MAT),sol)
#print ABCD

#A = ABCD[0]
#B = ABCD[1]
#C = ABCD[2]
#D = ABCD[3]

##PLot result
#psi = np.linspace(0,7.0*np.pi/4.0,1000)
#vhat = A*np.cos(psi) + B*np.cos(2*psi) + C*np.cos(3*psi) + D
##Easy Fix
#vhat[np.where((psi>135.0*np.pi/180.0) & (psi<225.0*np.pi/180.0))] = 0.0
###########################################################

###Read in Experimental Data
#data = IO.dlmread('/home/carlos/Documents/GitLab_Repos/Geophysical_Sampling/FASTPitot/Data_Files/Angle_Tests/Raw_Data_Extra_Data_Points.csv')
data = IO.dlmread('/home/carlos/Files/GitLab_Repos/Research/Geophysical_Sampling/FASTPitot/Data_Files/Angle_Tests/Raw_Data_Bad_360_Removed.csv')

if data is None:
    sys.exit()

##Plot empirical results from Matt 1/29/31
psi_exp = data[:,0]
#print psi_exp
##Plot Raw Data from 20 Hz and 35 Hz Data
plt.figure()
s = 0
v_exp_20 = np.zeros([len(psi_exp)])
v_exp_35 = np.zeros([len(psi_exp)])
for n in range(4):
    s+=2
    if s > 7:
        s = 0
    ##20 Hz Data
    #print data[:,n+1]
    v_exp_20_i = shift(data[:,n+1],s)
    #print v_exp_20_i
    ##Strip all the -99's
    ##Squash to +- 1
    v_exp_20_i /= np.max(abs(v_exp_20_i))
    ##Add to average
    v_exp_20 += v_exp_20_i
    
    ##35 Hz Data
    v_exp_35_i = shift(data[:,n+5],s)
    #print v_exp_35_i
    ##Squash to +- 1
    v_exp_35_i /= np.max(abs(v_exp_35_i))
    v_exp_35 += v_exp_35_i
    
    plt.scatter(psi_exp,v_exp_20_i,color='b',marker='o')
    plt.scatter(psi_exp,v_exp_35_i,color='r',marker='o')
  
##Compute averages from both figures
v_exp_35 /= 4.0
v_exp_20 /= 4.0

plt.plot(psi_exp,v_exp_20,color='b',marker='s',label='20 Hz Average')
plt.plot(psi_exp,v_exp_35,color='r',marker='s',label='35 Hz Average') 

##Average Between Experiments
v_exp_avg = 0.5*(v_exp_35+v_exp_20) 
  
###Average between symmetric points
v_exp_avg[[1,7]] = 0.5*(v_exp_avg[1] + v_exp_avg[7])
v_exp_avg[[2,6]] = 0.5*(v_exp_avg[2] + v_exp_avg[6])
v_exp_avg[[3,5]] = 0.5*(v_exp_avg[3] + v_exp_avg[5])
if len(v_exp_avg) == 9:
    v_exp_avg[[0,8]] = 0.5*(v_exp_avg[0] + v_exp_avg[8])
else:
    psi_exp = np.concatenate((psi_exp,[360]))
    v_exp_avg = np.concatenate((v_exp_avg,[v_exp_avg[0]]))
plt.plot(psi_exp,v_exp_avg,color='green',marker='o',label='Experiment Average+Symmetry')  

########Fourier Series NUMERICAL FIT#######################
 
# v = d + sum( an * cos ( wn * psi ) + bn * sin ( wn * psi) )
# wn = 2*pi*n / L
# L = 360 degrees or 2*pi
#d = np.mean(v_exp_avg)
#L = 2.0*np.pi
# [a1 b1 a2 b2 ... an bn]' = THETA --- our unknowns
# H = [cos(w1*psi) sin(w1*psi) ... cos(wn*psi) sin(w1*psi)]
# X = v-d
# X = H*THETA
# THETA = inv(H'*H)*H'*X
#X = v_exp_avg - d
#N = 3
#psi_exp_rad = psi_exp*np.pi/180.0
#H = np.zeros([len(psi_exp_rad),2*N])
#for n in range(N):
#    wn = 2.0*np.pi*(n+1)/L
#    H[:,2*n] = np.cos(wn*psi_exp_rad)
#    H[:,2*n+1] = np.sin(wn*psi_exp_rad)
#    print wn,2*n,2*n+1
##Solve for THETA
#print H
#HH = np.matmul(np.transpose(H),H)
#print 'HH=',HH
#invHH = np.linalg.inv(HH)
#print 'invHH=',invHH
#HX = np.matmul(np.transpose(H),X)
#print 'HX = ',HX
#THETA = np.matmul(invHH,HX)
#print 'THETA=',THETA

## Recreate Fit
#vfit = np.zeros(len(vhat))+d
#for n in range(N):
#    wn = 2.0*np.pi*(n+1)/L
#    vfit += THETA[2*n]*np.cos(wn*psi) + THETA[2*n+1]*np.sin(wn*psi)
    
########Fourier Series COS ONLY#######################
 
# v = d + sum( an * cos ( wn * psi ) 
# wn = 2*pi*n / L
# L = 360 degrees or 2*pi
d_COS = np.mean(v_exp_avg)
L = 2.0*np.pi
# [a1 b1 a2 b2 ... an bn]' = THETA --- our unknowns
# H = [cos(w1*psi) sin(w1*psi) ... cos(wn*psi) sin(w1*psi)]
# X = v-d
# X = H*THETA
# THETA = inv(H'*H)*H'*X
X = v_exp_avg - d_COS
N = 4
psi_exp_rad = psi_exp*np.pi/180.0
H = np.zeros([len(psi_exp_rad),N])
for n in range(N):
    wn = 2.0*np.pi*(n+1)/L
    H[:,n] = np.cos(wn*psi_exp_rad)
##Solve for THETA
#print H
HH = np.matmul(np.transpose(H),H)
#print 'HH=',HH
invHH = np.linalg.inv(HH)
#print 'invHH=',invHH
HX = np.matmul(np.transpose(H),X)
#print 'HX = ',HX
THETA_COS = np.matmul(invHH,HX)
print 'THETA=',THETA_COS

## Recreate Fit
psi = np.linspace(0,2*np.pi,1000)
vcos = np.zeros(len(psi))+d_COS
for n in range(N):
    wn = 2.0*np.pi*(n+1)/L
    vcos += THETA_COS[n]*np.cos(wn*psi)
    
########POLYNOMIAL FIT
# v = c0 + c1*x + c2*x^2 + ....cn*x^n
#c0 = np.mean(v_exp_avg)
# [c1 c2 c3 ....cn]' = THETA --- our unknowns
# H = [psi psi^2 psi^3 .... psi^n]
# X = v-c0
# X = H*THETA
# THETA = inv(H'*H)*H'*X
#X = v_exp_avg - c0
#N = 5
#psi_exp_rad = psi_exp*np.pi/180.0
#H = np.zeros([len(psi_exp_rad),N])
#for n in range(N):
#    H[:,n] = psi_exp_rad**(n+1)
#    print n
###Solve for THETA
#print H
#HH = np.matmul(np.transpose(H),H)
#print 'HH=',HH
#invHH = np.linalg.inv(HH)
#print 'invHH=',invHH
#HX = np.matmul(np.transpose(H),X)
#print 'HX = ',HX
#THETA = np.matmul(invHH,HX)
#print 'THETA=',THETA

## Recreate Fit
#vpoly = np.zeros(len(vhat))+c0
#for n in range(N):
#    vpoly += THETA[n]*psi**(n+1)

###PLOT RESULTS

#plt.plot(psi*180.0/np.pi,vhat,color='blue',label='Fourier Series (Hypothesis)')
#plt.plot(psi*180.0/np.pi,vfit,color='cyan',label='Fourier Series')
plt.plot(psi*180.0/np.pi,vcos,color='black',label='Cosine Series Fit')
#plt.plot(psi*180.0/np.pi,vpoly,color='black',label='Polynomial Fit')
#plt.scatter(psi_exp,v_exp_20,color='red',marker='o',label='Experiment 20 Hz')
#plt.scatter(psi_exp,v_exp_35,color='green',marker='o',label='Experiment 35 Hz')
#plt.scatter(psi_perfect,v_perfect,color='blue',marker='o',label='Hypothesis')

plt.grid()
plt.xlabel('Angle (deg)')
plt.ylabel('Magnitude Factor (nd)')
plt.legend()
plt.show()
