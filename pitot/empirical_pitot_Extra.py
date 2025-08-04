###This routine will generate the empirical formula for 
##one pitot probe
import numpy as np
import matplotlib.pyplot as plt
import mio as IO
import sys

plt.close("all")
plt.rcParams.update({'font.size': 14})

def wrap(indata):
    outdata = []
    for val in indata:
        if val > 360:
            val -= 360
        if val < 0:
            val += 360
        outdata.append(val)
    return np.asarray(outdata)

#data = IO.dlmread('/home/carlos/Documents/GitLab_Repos/Geophysical_Sampling/FASTPitot/Data_Files/Angle_Tests/Raw_Data_Extra_No_Processing.csv')
data = IO.dlmread('/home/files/Docs/GitLab_Repos/Research/Geophysical_Sampling/FASTPitot/Data_Files/Angle_Tests/Raw_Data_Extra_No_Processing.csv')

##Get heading
psi_exp = data[:,0]
##Wrap Psi
psi_exp_wrap = wrap(psi_exp)
###And Let's sort it
psi_exp_wrap_sort = np.sort(psi_exp_wrap)

###Plot Raw Data
plt.figure()
##Get averaging ready
v_exp_20 = np.zeros([len(psi_exp)])
v_exp_35 = np.zeros([len(psi_exp)])
for x in range(1,5):
    #Extract Raw Data
    v_exp_20_i = data[:,x]
    v_exp_35_i = data[:,x+4]
    ##Unfortunately Not every pitot probe is aligned with 
    ##unit North. So they need to be rotated individually
    ##Don't need to do the last data point
    if x < 4:
        psi_exp_i = psi_exp - 90*x
    else:
        psi_exp_i = psi_exp
    ##Then we need to wrap again
    psi_exp_wrap_i = wrap(psi_exp_i)
    #print psi_exp_wrap_i
    ##To make sure everything lines up properly we will sort
    ##this array
    index = np.argsort(psi_exp_wrap_i)
    ##And plot the sorted arrays
    psi_exp_wrap_sort_i = psi_exp_wrap_i[index]
    v_exp_20_sort_i = v_exp_20_i[index]
    v_exp_35_sort_i = v_exp_35_i[index]
    #print psi_exp_wrap_sort_i
    #print v_exp_20_sort_i
    #Normalize Data
    v_exp_20_sort_i /= np.mean(abs(v_exp_20_sort_i[[0,2,3,8,9,11]]))
    v_exp_35_sort_i /= np.mean(abs(v_exp_35_sort_i[[0,2,3,8,9,11]]))
    ##Now we average it
    v_exp_20 += v_exp_20_sort_i
    v_exp_35 += v_exp_35_sort_i
    ##Plot it
    #print psi_exp_wrap_sort_i
    plt.scatter(psi_exp_wrap_sort_i,v_exp_20_sort_i,color='b',marker='o')
    plt.scatter(psi_exp_wrap_sort_i,v_exp_35_sort_i,color='r',marker='o')

##Compute averages from both figures
v_exp_35 /= 4.0
v_exp_20 /= 4.0

###Unfortunately this isn't enough. When you go take data past 315 degrees
##You end up getting repeated data points
#psi_unique, indices = np.unique(psi_exp_wrap_sort, return_index=True)
#print indices
##Ok now we need to loop through indices
psi_unique = []
v_exp_20_unique = []
v_exp_35_unique = []
for x in range(0,len(psi_exp_wrap_sort)-1):
    ##Check for a repeated value
    if psi_exp_wrap_sort[x] == psi_exp_wrap_sort[x+1]:
        #print 'Repeated Value'
        ##We need to grab psi from both to make sure
        #print psi_exp_wrap_sort[x],psi_exp_wrap_sort[x+1]
        ##Now we grab data from 20 and 35 Hz
        #print v_exp_20[x],v_exp_20[x+1]
        #print v_exp_35[x],v_exp_35[x+1]
        ##Average them together
        avg_20 = (v_exp_20[x]+v_exp_20[x+1])*0.5
        avg_35 = (v_exp_35[x]+v_exp_35[x+1])*0.5
    else:
        ##Otherwise just grab the current data point
        avg_20 = v_exp_20[x]
        avg_35 = v_exp_35[x]
        
    if psi_exp_wrap_sort[x] != psi_exp_wrap_sort[x-1]:
        ##Append everything to outvectors provided this data point
        ##Is not the same as the last data point
        psi_unique.append(psi_exp_wrap_sort[x])
        v_exp_20_unique.append(avg_20)
        v_exp_35_unique.append(avg_35) 
    
##Append the last data point
v_exp_20_unique.append(v_exp_20[-1])
v_exp_35_unique.append(v_exp_35[-1])
psi_unique.append(psi_exp_wrap_sort[-1]) 
    
#Convert everything to numpy arrays
psi_u = np.asarray(psi_unique)
v_exp_20_u = np.asarray(v_exp_20_unique)
v_exp_35_u = np.asarray(v_exp_35_unique)

plt.plot(psi_u,v_exp_20_u,color='b',marker='s',label='Scaled 20 Hz Average')
plt.plot(psi_u,v_exp_35_u,color='r',marker='s',label='Scaled 35 Hz Average') 

##Average Between Experiments
v_exp_u = 0.5*(v_exp_35_u+v_exp_20_u) 
plt.plot(psi_u,v_exp_u,color='cyan',marker='o',label='Average Between 20 and 35 Hz')

###Average between symmetric points
v_exp_u[[1,7]] = 0.5*(v_exp_u[1] + v_exp_u[7])
v_exp_u[[2,6]] = 0.5*(v_exp_u[2] + v_exp_u[6])
v_exp_u[[3,5]] = 0.5*(v_exp_u[3] + v_exp_u[5])
if len(v_exp_u) == 9:
    v_exp_u[[0,8]] = 0.5*(v_exp_u[0] + v_exp_u[8])
else:
    psi_u = np.concatenate((psi_u,[360]))
    v_exp_u = np.concatenate((v_exp_u,[v_exp_u[0]]))
plt.plot(psi_u,v_exp_u,color='green',marker='o',label='Averaging using Symmetry')  

##Alright now do the fourier series fit
########Fourier Series COS ONLY#######################
 
# v = d + sum( an * cos ( wn * psi ) 
# wn = 2*pi*n / L
# L = 360 degrees or 2*pi
d_COS = np.mean(v_exp_u)
print d_COS
L = 2.0*np.pi
# [a1 b1 a2 b2 ... an bn]' = THETA --- our unknowns
# H = [cos(w1*psi) sin(w1*psi) ... cos(wn*psi) sin(w1*psi)]
# X = v-d
# X = H*THETA
# THETA = inv(H'*H)*H'*X
X = v_exp_u - d_COS
N = 4
psi_exp_rad = psi_u*np.pi/180.0
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

###And plot it
plt.plot(psi*180.0/np.pi,vcos,color='black',label='Cosine Series Fit')

##Add some extra
plt.grid()
plt.xlabel('Angle (deg)')
plt.ylabel('Magnitude Factor (nd)')
plt.legend(loc='best')

plt.show()