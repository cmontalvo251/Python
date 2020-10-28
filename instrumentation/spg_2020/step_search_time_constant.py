import numpy as np
import matplotlib.pyplot as plt

cool = np.loadtxt('Cool_Down.txt')
time_cool = cool[:,0]
time_cool-=time_cool[0]
temp_cool = cool[:,1]
time_cool_clipped = time_cool[time_cool>23]
temp_cool = temp_cool[time_cool>23]
time_cool_clipped-=time_cool_clipped[0]


plt.figure()

###Initial Guess
residual_optimal = 1e200

###Time Constant
Ta = -8.44
T0 = 26.5
time_cool_sim = np.linspace(0,time_cool_clipped[-1],1000)
for TsC in np.linspace(1,1000,100):
    plt.cla()
    
    #TsC = 720-t0
    tauC = 4./TsC

    ##Plot raw data
    plt.plot(time_cool_clipped,temp_cool,'b*',label='Measured Data')
    
    ##Clean up
    plt.grid()
    plt.xlabel('Time (sec)')
    plt.ylabel('Temperature (C)')
    
    temp_cool_sim = (Ta-T0)*(1-np.exp(-tauC*time_cool_sim)) + T0
    
    temp_cool_interpolate = (Ta-T0)*(1-np.exp(-tauC*time_cool_clipped)) + T0
    
    residuals = (temp_cool_interpolate - temp_cool)**2
    
    print(TsC,np.sum(residuals))
    
    if np.sum(residuals) < residual_optimal:
        residual_optimal = np.sum(residuals)
        print('New Optimum found')
        tauOpt = tauC
        temp_cool_opt = (Ta-T0)*(1-np.exp(-tauOpt*time_cool_sim)) + T0
    
    plt.plot(time_cool_sim,temp_cool_sim,'r-',label='Fitted Data')
    plt.plot(time_cool_sim,temp_cool_sim,'rs',label='Interpolated Data')
    
    ##plot the optimal solution in green
    plt.plot(time_cool_sim,temp_cool_opt,'y-',label='Optimal Solution')
    
    ###Least Square Regression
    ### cost function = J = residuals
    ### Minimizes J
    ### Spits out the solution to minimizing res
    ### Compute r^2 OR minimize res
    
    plt.legend()
    plt.pause(0.0001)

print('Optimal tau =',tauOpt)
plt.show()