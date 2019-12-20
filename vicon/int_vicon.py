#!/usr/bin/python

import vicon as V 
import matplotlib.pyplot as plt 
import sys 
from pdf import *
import plotting as P 


if __name__ == "__main__":

#Get input arguments
	if len(sys.argv) > 2:
    		 viconFile = sys.argv[1]
    	numMarkers = int(sys.argv[2])
    	
	
	pp = PDF(0,plt)

	vicon_data = V.get_vicon_data(viconFile,numMarkers)
	time_vicon = vicon_data.t
	time_vicon -= time_vicon[0]
	vicon_acc = vicon_data.yddot

	#integrate yddot to velocity then integrate that to positiion 

	vicon_pos = [0]
	vicon_vel = [0]

	for idx in range(0,len(vicon_acc)-1):
		h = time_vicon[idx+1] - time_vicon[idx]
		current = vicon_vel[-1] + vicon_acc[idx]*h
		vicon_vel.append(current)
	for jdx in range(0,len(vicon_vel)-1):
		h = time_vicon[jdx+1] - time_vicon[jdx]
		now = vicon_pos[-1] + vicon_vel[jdx]*h
		vicon_pos.append(now)
	print len(vicon_acc)/time_vicon[-1]
	print len(vicon_vel)
	print len(vicon_pos)

	figure = plt.figure()
	plt.plot(time_vicon,vicon_acc,label = 'Acceleration (m/s^2)')
	plt.grid()
	plt.xlabel('Time (s)')
	plt.ylabel('Acceleration')
	plt.ylim([-40,40])
	pp.savefig()
	
	figure0 = plt.figure()
	plt.plot(time_vicon,vicon_vel,label = 'Integrated Velocity (m/s)')
	plt.plot(time_vicon,vicon_data.ydot,label = 'Vicon Velocity (m/s)')
	
	plt.grid()
	plt.legend()
	plt.xlabel('Time (s)')
	plt.ylabel('Velocity (m/s)') 
	pp.savefig()

	figure1 = plt.figure()
	plt.plot(time_vicon,vicon_pos,label = 'Integrated Position (m)')
	plt.plot(time_vicon,vicon_data.y,label = 'Vicon Position (m)')
	plt.grid()
	plt.legend()
	plt.xlabel('Time (s)')
	plt.ylabel('Postion (m)')
	pp.savefig()
	pp.close()