#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 13:39:01 2021

@author: carlos
"""
import numpy as np
import matplotlib.pyplot as plt
accel_data = np.loadtxt('accel_data.csv',delimiter=',')
x = accel_data[:,0]
y = accel_data[:,1]
z = accel_data[:,2]
dt = 0.1
endtime = len(x)*dt
t = np.arange(0,endtime,dt)
plt.plot(t,x)
plt.plot(t,y)
plt.plot(t,z)