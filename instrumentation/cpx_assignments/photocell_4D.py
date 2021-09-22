import numpy as np
import matplotlib.pyplot as plt
pdata = np.loadtxt('example_photo_cell_data.txt')

pos = pdata[:,0]
photocell_voltage = pdata[:,1:]

## POSITION = A0 * vp0 + A1 * vp1 + A2 * vp2 + A3 * vp3 ## 4th dimensional polynomial
## POSITION = [pdata] * [A0; A1;A2;A3] --- regression equation
## A = [A0; A1;A2;A3]
## A = ([pdata]T*pdata)^-1 - I could go on
## This is very complex.

#for x in range(0,4):
plt.figure()
  #  plt.plot(pos,photocell_voltage[:,x])
plt.plot(photocell_voltage)
plt.grid()
plt.xlabel('Position')
plt.ylabel('Voltage')
plt.show()