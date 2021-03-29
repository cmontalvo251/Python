import numpy as np
import matplotlib.pyplot as plt

def speed_linear(voltage):
    return 1.49*voltage - 14.74

def speed_quadratic(voltage):
    return -0.0675*voltage**2 + 3.833*voltage - 34.29

volt = np.asarray([12,13,14,15,16,17,18,19,23])  ##voltage applied to motor
speed = np.asarray([3.0,3.5,5.0,8.0,10.0,11.5,13.5,14.0,18.0]) #speed in m/s

coeff = np.polyfit(volt,speed,2)

volt_fit = np.linspace(np.min(volt),np.max(volt),100)
speed_fit = np.polyval(coeff,volt_fit)

speed_manual_linear = speed_linear(volt_fit)
speed_manual_quadratic = speed_quadratic(volt_fit)

plt.plot(volt,speed,'b*',label='Experimental Data')
plt.plot(volt_fit,speed_fit,'r-',label='Trend Line Fit')
plt.plot(volt_fit,speed_manual_linear,'k-',label='Manually Entering Trend Line (Linear)')
plt.plot(volt_fit,speed_manual_quadratic,'y-',label='Manually Entering Trend Line (Quadratic)')
plt.grid()
plt.legend()
plt.title('Coeff = '+str(coeff))
plt.xlabel('Voltage (V)')
plt.ylabel('Speed (m/s)')

###Compute Residuals
speed_at_exp_data_pts = np.polyval(coeff,volt)
residuals = speed - speed_at_exp_data_pts

plt.figure()
plt.plot(volt,residuals,'b*')
plt.grid()
plt.xlabel('Voltage (V)')
plt.ylabel('Residuals (m/s)')



plt.show()