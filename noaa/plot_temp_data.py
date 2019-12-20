import numpy as np
import matplotlib.pyplot as plt


#Data from ----- https://www.ncdc.noaa.gov/cag/city/time-series/USW00013894/tmax/all/1/1948-2019?base_prd=true&firstbaseyear=1948&lastbaseyear=2000
data = np.loadtxt('USW00013894-tmax-all-1-1948-2019.txt',delimiter=',')
size = np.shape(data)
print(size)

num_months = size[0]

num_years = int(num_months/12)

print('Plotting Years = ',num_years)

ctr = 0

months = np.arange(1,13)

average = 0.0*months
num = 0.0

for idx in range(0,num_years):
    print('Plotting Year = ',data[ctr,0])
    temp = data[ctr:ctr+12,1]
    if num_years - idx < 10:
        plt.plot(months,temp,label=data[ctr,0])
    else:
        average += temp
        num+=1.0
    ctr+=12

average /= num

plt.plot(months,average,linewidth=5.0,label='Average')
plt.legend()
plt.grid()
plt.xlabel('Month')
plt.ylabel('Temp (F)')
plt.show()
    
    
