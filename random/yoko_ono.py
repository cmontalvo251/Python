import numpy as np
import matplotlib.pyplot as plt

time_race1 = 600.0

trace1 = np.linspace(0,time_race1*1.12,100)
distance_yolando = 100.0
speed_yolando = distance_yolando / time_race1
distance_yolando = speed_yolando*trace1
plt.plot(trace1,distance_yolando,'b-',label='Yolando Race1')

distance_yoko = 90.0
speed_yoko = distance_yoko / time_race1
distance_yoko = speed_yoko*trace1
plt.plot(trace1,distance_yoko,'r-',label='Yoko Race1')


distance_yolando2 = distance_yolando - 10.0

plt.plot(trace1,distance_yolando2,'g-',label='Yolando Race2')
plt.legend()
plt.ylim([-10,100])
plt.grid()
plt.show()