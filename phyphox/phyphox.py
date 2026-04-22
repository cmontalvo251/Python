###Read and plot csv phyphox data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##Load the data first
df = pd.read_csv('Accelerometer.csv')

print(df.head())

time = df['Time (s)']
ax = df['Acceleration x (m/s^2)']

plt.figure()
plt.plot(time,ax)
plt.xlabel('Time (sec)')
plt.ylabel('Acceleration (m/s^2)')
plt.title('Accelerometer Data')
plt.show()