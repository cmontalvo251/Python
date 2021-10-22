import os
import numpy as np
import matplotlib.pyplot as plt

time = []
temp = []

for root,dirs,files in os.walk('./'):
	for fname in files:
#		print(fname)
                splits = os.path.splitext(fname)
                filename = splits[0]
                extension = splits[1]
                if extension == '.csv':
                        fullpath = root +'/'+ fname
                        print(fullpath)
                        data = np.loadtxt(fullpath,delimiter=',')
                        print(data)
                        time = np.hstack((time,data[:,0]))
                        temp = np.hstack((temp,data[:,1]))

print(time)
print(temp)


plt.plot(time,temp)
plt.show()
